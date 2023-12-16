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

import importlib
import io
import time
import typing
import traceback
import logging
from contextlib import redirect_stdout, redirect_stderr

import yaml
from typing import Dict, Any, Union, List
import requests

from flask import current_app

if typing.TYPE_CHECKING:
    from ..models import Callback, CallbackExecution

NoneType = type(None)


CleanedConfigType = Dict[str, Union[
    bool,
    float,
    int,
    str,
    NoneType,
    List[Union[bool, float, int, str, NoneType]],
    Dict[str, Union[bool, float, int, str, NoneType]]
]]


def replace_mapping(string: str, mapping: typing.Mapping[str, str]):
    """
    Performs multiple substitutions in a string, will use each key-value pair
    a replacements.

    :param string: String to perform substitutions on
    :param mapping: The mapping containing all replacements pairs
    :return: Updated string after replacements
    """
    # Can't replace in a non-string
    if not isinstance(string, str):
        return string

    for key, value in mapping.items():
        string = string.replace(key, value)
    return string


def clean_value(value: Union[bool, float, int, str, NoneType]) -> Union[bool, float, int, str, NoneType]:
    if isinstance(value, bool):
        return bool(value)
    elif isinstance(value, float):
        return float(value)
    elif isinstance(value, int):
        return int(value)
    elif isinstance(value, str):
        return str(value)
    elif isinstance(value, NoneType):
        return None


def clean_config(config: Dict[str, Any]) -> CleanedConfigType:
    """
    Clean a config so that it is guaranteed to be serializable
    """
    cleaned_config = {}
    for key, value in config.items():
        if isinstance(value, (bool, float, int, str, NoneType)):
            cleaned_config[key] = clean_value(value)
        elif isinstance(value, (tuple, list, set)) and all(isinstance(x, (bool, float, int, str, NoneType)) for x in value):
            cleaned_config[key] = list(clean_value(x) for x in value)
        elif isinstance(value, dict) and all(isinstance(x, (bool, float, int, str, NoneType)) for x in value.values()):
            cleaned_config[key] = clean_config(value)
        else:
            current_app.logger.info(f'Dropping unclean {key}: [{type(value)}] {value}')

    return cleaned_config


def dispatch_callback(callback_execution: 'CallbackExecution',
                      config: Dict[str, Any]):
    """
    Dispatch the callback to the appropriate backend.
    """
    callback: 'Callback' = callback_execution.callback  # Typehint because it's a backreference
    callback_method_name = config.get("STUDYGOV_CALLBACK_METHOD")
    callback_function = CALLBACK_BACKENDS.get(callback_method_name, 'celery_backend')
    current_app.logger.info(f'Using callback function {callback_function} with '
                            f'method {callback.function} and callback execution {callback_execution.uri()}')

    # Remove non JSON serializable stuff from the config so things like celery won't choke on it
    cleaned_config = clean_config(config)

    callback_function(callback.function,
                      callback.callback_arguments,
                      callback_execution.uri(),
                      callback_execution.secret_key,
                      cleaned_config)


def update_callback_execution(url, secret, data):
    json_data = dict(data)
    json_data['secret'] = secret
    logging.debug(f'Updating callback execution %s with %s', url, data)
    response = requests.put(url, json=json_data)
    if response.status_code not in [200, 201]:
        raise ValueError(f'Could not update callback execution, response: [{response.status_code}] {response.text}')


def master_callback(*,
                    callback_function: str,
                    callback_arguments: str,
                    callback_execution_url: str,
                    callback_execution_secret: str,
                    config: Dict[str, Any]):

    # Update callback state to running
    logging.info(f'Setting {callback_execution_url} status to running')
    update_callback_execution(
        url=callback_execution_url,
        secret=callback_execution_secret,
        data={'status': 'running'},
    )

    callback_output = io.StringIO()
    with redirect_stdout(callback_output), redirect_stderr(callback_output):
        try:
            # Load the callback function and parse the arguments
            callback_data = yaml.safe_load(callback_arguments)
            callback_module = importlib.import_module(f'.{callback_function}', 'studygovernor.callbacks')
            callback = getattr(callback_module, callback_function)

            # Get the callback execution data
            response = requests.get(callback_execution_url, json={'secret_key': callback_execution_secret})
            if response.status_code != 200:
                raise ValueError('Could not retrieve callback execution information!')

            # Get callback execution data and add secret for the callback function in case it
            # needs to be queried again
            callback_execution_data = response.json()
            callback_execution_data['secret'] = callback_execution_secret

            logging.debug('Calling callback with initial_delay: %s', callback_execution_data['callback']['initial_delay'])
            logging.debug('Calling callback with callback_execution_data: %s', callback_execution_data)
            logging.debug('Calling callback with config: %s', config)
            logging.debug('Calling callback with callback_data: %s', callback_data)
            # Get initial delay and wait if needed
            delay = callback_execution_data['callback']['initial_delay']
            if delay:
                time.sleep(delay)

            # Call the actual callback function
            return_values = callback(callback_execution_data, config, **callback_data)
            if '__success__' not in return_values:
                return_values['__success__'] = True

        except Exception as exception:
            return_values = {
                '__success__': False,
                '__exception__': str(exception),
                '__traceback__': traceback.format_exc()
            }
            logging.error('Error running callback: %s', callback_function)
            logging.error('Exception: %s', str(exception))
            logging.error('Traceback: %s', traceback.format_exc())

    success = return_values.get('__success__', True)

    # Collect stdout/stderr from the run
    run_log = callback_output.getvalue()
    wait_timeout = callback_execution_data['callback']['wait_timeout']

    # Update callback state to running, check if we need to wait or the
    # timeout has finished.
    if not success:
        status = 'finished'
        result = 'failed'
    elif wait_timeout == 0:
        status = 'finished'
        result = 'success'
    else:
        status = 'waiting'
        result = 'none'

    payload = {
        'status': status,
        'result': result,
        'result_values': return_values,
        'run_log': run_log,
    }

    update_callback_execution(
        url=callback_execution_url,
        secret=callback_execution_secret,
        data=payload
    )


# Empty backends dictionary to be populated
CALLBACK_BACKENDS = {}

# Register the celery callback backend
from .backends import local_backend
from .backends import celery_backend
