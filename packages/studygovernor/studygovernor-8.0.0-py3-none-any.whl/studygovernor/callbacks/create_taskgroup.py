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
import os
from string import Template
from typing import Dict, Any, Optional

import logging

from .create_task import check_extra_tags, taskmanager_post


def create_taskgroup(callback_execution_data,
                     config: Dict[str, Any],
                     label,
                     tasks,
                     distribute_in_group=None,
                     distribute_method=None,
                     tags=None,
                     project=None,
                     xnat_external_system: str='XNAT',
                     taskmanager_external_system_name: str='TASKMANAGER',
                     extra_tags_var: Optional[str] = None,
                     **ignore) -> Dict[str, Any]:
    """
    Create taskmanager task

    :param callback_execution_data: All data needed about the callback execution
    :param config: App configuration
    :param label: label of the created task group
    :param tasks: a list of tasks to create, each should be a dict with base, template and tags defined
    :param distribute_in_group: group the tasks should be distributed in
    :param distribute_method: the method of distributed to use
    :param tags: list of tags to add to each tasks in the taskgroup
    :param project: the project for the tasks in the taskgroup
    :param xnat_external_system: name of the external xnat [XNAT]
    :param taskmanager_external_system_name: Taskmanager external ID [TASKMANAGER]

    Example:

    .. code-block:: YAML

        function: create_taskgroup
        callback_arguments:
            label: 123_inspect
            distribute_in_group: raters
            tags: [rss, inspect]
            project: RSS
            tasks:
                - base: base_tissue.json
                  template: tissuewml
                  tags: [rss, tissue]
                - base: base_mask.json
                  template: mask
                  tags: [rss, mask]
                  project: OVERWRITE
                - base: base_lobes.json
                  template: lobes
                  tags: [rss, lobes]
            extra_tags_var: tag_variable


    Return values of this callback is:

    ==================== ====== ===================================================================
    Variable name        Type   Description
    ==================== ====== ===================================================================
    response_status_code int    Response code for the request to the taskmanager
    response_text        str    Response text for the request to the taskmanager
    task_info            dict   Task info sent to the taskmanager to create the task group
    task_uri             str    URI of the newly created task
    ==================== ====== ===================================================================
    """
    if tags is None:
        tags = []

    # Get External system urls
    logging.debug(f"Starting callback for action_url: {callback_execution_data['uri']}")
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

    # Read extra tags variable to find extra tags
    extra_tags = check_extra_tags(experiment=experiment, extra_tags_var=extra_tags_var)

    # Inject extra tags in task_info
    if extra_tags:
        tags.extend(x for x in extra_tags if x not in tags)

    # Get task base from the correct directory
    # task_bases = os.listdir(config['STUDYGOV_PROJECT_TASKS'])
    task_bases = os.listdir(config['STUDYGOV_PROJECT_TASKS'])

    tasks_data = []
    callback_url = callback_execution_data["api_uri"]
    callback_content = json.dumps({
        "status": "finished",
        "result": "success",
        "secret_key": callback_execution_data["secret"]
    })

    for task in tasks:
        # Inject the generator_url (= action_url) in the task_info, combine tags, copy other fields
        task_info = {
            'tags': tags + [x for x in task.get('tags', []) if x not in tags],
            'project': task.get('project') or project,  # Can set at taskgroup or overriden at task level
            'callback_url': task.get('callback_url', callback_url),
            'callback_content': '',
            'template': task.get('template'),
            'generator_url': callback_execution_data['web_uri'],
        }

        if task_info['callback_url']:
            task_info['callback_content'] = callback_content

        if 'application_name' in task:
            task_info['application_name'] = task['application_name']

        if 'application_version' in task:
            task_info['application_version'] = task['application_version']

        # Fill task content using the base
        task_base = task['base']

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
                                                      LABEL=experiment['label'],
                                                      SYSTEM_URL=xnat_server)

        # Update fields with per-experiment information
        task_info['content'] = task_content

        tasks_data.append(task_info)

    url = '{url}/api/v1/taskgroups'.format(url=task_manager_server)

    taskgroup = {
        'label': label,
        'tasks': tasks_data,
    }

    # Distribute info is optional
    if distribute_in_group is not None:
        taskgroup['distribute_in_group'] = distribute_in_group

    if distribute_method is not None:
        taskgroup['distribute_method'] = distribute_method

    # Callback data is required
    taskgroup['callback_url'] = callback_execution_data["api_uri"]

    # Set callback content for updating finished
    taskgroup['callback_content'] = callback_content

    response = taskmanager_post(url=url, json=taskgroup)

    # Set the progress state
    logging.debug(f"Finished callback for url: {callback_execution_data['uri']}")

    response_data = response.json()
    print(response_data)

    return {
        'response_status_code': response.status_code,
        'response_text': response.text,
        'task_info': taskgroup,
        'task_uri': response_data['uri'],
    }
