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

import subprocess
from typing import Any, Dict

from flask import current_app

from studygovernor.callbacks import CALLBACK_BACKENDS


def local_callback(*,
                   callback_function: str,
                   callback_arguments: str,
                   callback_execution_url: str,
                   callback_execution_secret: str,
                   config: Dict[str, Any]):
    """
    This function dispatches a callback, at the moment it just creates a subprocess to handle the callback

    :param str callback_function: Function for this callback
    :param str callback_arguments: Arguments for the callback
    :param str callback_execution_url: URL of the callback execution to run
    :param str callback_execution_secret: Secret key to get access to this callback execution
    :param dict config: Copy of (most of) the flask app config
    :return:
    """
    # TODO: move this to a background watchdog thread that makes sure the program doesn't hang
    #       and can kill it when needed?
    current_app.logger.info('Local callback: {action_url}')
    callback_process = subprocess.Popen(['studygov-run-callback',
                                         '-c', callback_execution_url])


CALLBACK_BACKENDS['local'] = local_callback

