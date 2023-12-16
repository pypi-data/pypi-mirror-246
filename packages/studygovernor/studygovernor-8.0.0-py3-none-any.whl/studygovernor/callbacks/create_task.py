# Copyright 2017 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import netrc
import os
from string import Template
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse

import requests

import logging


def check_extra_tags(experiment: Dict,
                     extra_tags_var: Optional[str]) -> List[str]:
    extra_tags = []
    if extra_tags_var:
        extra_tags = experiment['variable_map'].get(extra_tags_var)

        if extra_tags is not None:
            if isinstance(extra_tags, str):
                extra_tags = [extra_tags]
            if not isinstance(extra_tags, list):
                logging.error('Extra tags retrieval failed, setting extra tags to []')
                extra_tags = []

    return extra_tags


def taskmanager_post(url: str, json: Dict) -> requests.Response:
    # Check if there is login information in netrc
    netloc = urlparse(url).netloc
    try:
        auth_info = netrc.netrc().authenticators(netloc)
    except IOError:
        auth_info = None

    print('Found auth_info for {}: {}'.format(netloc, auth_info is not None))

    # Send the task to the task manager
    if auth_info is None:
        response = requests.post(url, json=json)
    else:
        response = requests.post(url, json=json, auth=(auth_info[0], auth_info[2]))

    if response.status_code not in [200, 201]:
        raise ValueError(f'POST request to {url} lead to response with invalid status: [{response.status_code}]: {response.text}')

    return response


def create_task(callback_execution_data,
                config: Dict[str, Any],
                task_base,
                task_info,
                extra_tags_var: Optional[str] = None,
                xnat_external_system: str = 'XNAT',
                taskmanager_external_system_name: str = 'TASKMANAGER',
                **ignore) -> Dict[str, Any]:
    """
    Create taskmanager task

    :param callback_execution_data: callback execution data
    :param config: flask app configuration dict
    :param task_base: task_base is a Template that contains info for the task
    :param task_info: Additional info for the task as a list of [key1 val1 key2 val2 ...]
    :param extra_tags_var: Name of variable (in experiment) from which to extract extra tags
    :param xnat_external_system: name of the external xnat [XNAT]
    :param taskmanager_external_system_name: Taskmanager external ID [TASKMANAGER]

    Example:

    .. code-block:: YAML

      function: create_task
      callback_arguments:
        task_base: manual_qa.json,
        task_info:
          project: sandbox
          application_name: ViewR
          application_version: 5.1.4
          template: manual_qa
          tags: ["QA", "Quality Assurance"]
          distribute_in_group: quality_assurance
        extra_tags_var: tag_variable
        xnat_external_system: XNAT
        taskmanager_external_system_name: TASKMANAGER

    If ``extra_tags_var`` is ``tag_variable``, the value of ``experiment.variable_map[tag_variable]`` is
    used to define extra tags. If the variable is not set for the experiment it is ignore. The resulting
    value should be a string or list of string (in which case multiple tags are added).

    Return values of this callback is:

    ==================== ====== ===================================================================
    Variable name        Type   Description
    ==================== ====== ===================================================================
    response_status_code int    Response code for the request to create the task on the taskmanager
    response_text        str    Response text for the request to create the task on the taskmanager
    task_info            dict   Task info sent to the taskmanager to create the task
    task_uri             str    URI of the newly created task
    ==================== ====== ===================================================================
    """
    # Get External system urls
    logging.debug(f"Starting callback for callback execution: {callback_execution_data['uri']}")
    xnat_server = callback_execution_data['external_systems'][xnat_external_system].rstrip('/')
    task_manager_server = callback_execution_data['external_systems'][taskmanager_external_system_name].rstrip('/')
    logging.debug(f"Using xnat: {xnat_server}")
    logging.debug(f"Using taskmanager: {task_manager_server}")

    # Get required information
    experiment = callback_execution_data['experiment']
    subject = callback_execution_data['subject']
    print(f"Experiment located at: {experiment['uri']}")
    xnat_experiment_id = experiment['external_ids'][xnat_external_system]
    xnat_subject_id = subject['external_ids'][xnat_external_system]
    label = experiment['label']

    # Check if extra tags need to be added
    extra_tags = check_extra_tags(experiment=experiment,
                                  extra_tags_var=extra_tags_var)

    # Inject extra tags in task_info
    if extra_tags:
        if 'tags' in task_info:
            task_info['tags'].extend(extra_tags)
        else:
            task_info['tags'] = extra_tags

    # Inject the generator_url (= action_url) in the task_info
    task_info['generator_url'] = callback_execution_data['web_uri']

    # Get task base from the correct directory
    task_bases = os.listdir(config['STUDYGOV_PROJECT_TASKS'])

    if task_base in task_bases:
        task_base_file = os.path.join(config['STUDYGOV_PROJECT_TASKS'], task_base)
    else:
        raise ValueError('Task base "{}" not found!'.format(task_base))

    # Read the file and fill out the base
    print('Loading taskbase file {}'.format(task_base_file))
    with open(task_base_file) as input_file:
        task_base = input_file.read()

    task_content = Template(task_base).substitute(EXPERIMENT_ID=xnat_experiment_id,
                                                  SUBJECT_ID=xnat_subject_id,
                                                  LABEL=label,
                                                  SYSTEM_URL=xnat_server)

    # Update fields with per-experiment information
    task_info['tracking_id'] = label
    task_info['content'] = task_content
    task_info['callback_url'] = callback_execution_data["api_uri"]

    # Set callback content for updating finished
    task_info['callback_content'] = json.dumps({
        "status": "finished",
        "result": "success",
        "secret_key": callback_execution_data["secret"]
    })

    url = '{url}/api/v1/tasks'.format(url=task_manager_server)

    logging.debug(f"Finished callback for url: {callback_execution_data['uri']}")

    response = taskmanager_post(url=url, json=task_info)
    response_data = response.json()

    return {
        'response_status_code': response.status_code,
        'response_text': response.text,
        'task_info': task_info,
        'task_uri': response_data['uri'],
    }
