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
import re
import subprocess
from typing import Mapping, Sequence, Dict, Any

from . import replace_mapping


def command(callback_execution_data,
            config: Dict[str, Any],
            binary: str,
            args: Sequence[str]=None,
            kwargs: Mapping[str, str]=None,
            xnat_external_system_name: Any='XNAT',
            **ignore) -> Dict[str, Any]:
    """
    Calls a command. This can be any command that is on the PATH of the StudyGovernor (worker) environment.

    .. warning:: It is strongly recommened to use the ``external_program`` callback instead of possible, as its
                 behaviour is a lot more predicable and reproducible.

    The binary gets the command in the form:

    .. code-block:: bash

       binary $ARGS $KWARGS

    :param callback_execution_data: callback execution data
    :param config: flask app configuration dict
    :param binary: binary that gets executed
    :param args: list of args [val1 val2 ...]
    :param kwargs: list of [key1 val1 key2 val2 ...]
    :param xnat_external_system_name: name of the external xnat [XNAT]

    The items in args and values in kwargs that contain certain VARS will be replaced. Accepted VARS:

    The items in args and values in kwargs that contain certain VARS will be replaced. Accepted VARS:

    - ``$EXPERIMENT``: will be substituted with the experiment URL.
    - ``$SUBJECT``: will be substituted with the subject URL.
    - ``$XNAT``: will be substituted with the XNAT URL.
    - ``$CALLBACK_EXECUTION``: Will be substituted with the callback execution URL
    - ``$CALLBACK_SECRET``: Will be substituted with the callback execution secret


    Example:

    .. code-block:: YAML

      function: command
      callback_arguments:
        binary: check.py
        args:
          - $CALLBACK_EXECUTION
          - $CALLBACK_SECRET
        kwargs:
          -x: "$XNAT"


    Result of the callback is:

    ==================== ====== ===================================================================
    Variable name        Type   Description
    ==================== ====== ===================================================================
    command              list   The command represented as a list of strings
    stdout               str    The stdout of the called process
    stderr               str    The stderr of the called process
    return_code          int    The return code of the called process
    ==================== ====== ===================================================================
    """
    args = args or []
    kwargs = kwargs or {}

    # Get XNAT address from database
    xnat_uri = callback_execution_data['external_systems'][xnat_external_system_name].rstrip('/')

    # Define replacements available
    replacements = {
        "$XNAT": xnat_uri,
        "$EXPERIMENT": callback_execution_data['experiment']['api_uri'],
        "$SUBJECT": callback_execution_data['subject']['api_uri'],
        "$CALLBACK_EXECUTION": callback_execution_data['api_uri'],
        "$CALLBACK_SECRET": callback_execution_data['secret'],
    }

    # Substitute variables in arguments
    args = [replace_mapping(x, replacements) for x in args]
    kwargs = {k: replace_mapping(v, replacements) for k, v in kwargs.items()}

    # Build the command and execute
    command = [binary] + [str(x) for x in args] + [str(x) for k, v in kwargs.items() for x in [k, v]]

    print('Calling command: {}'.format(command))
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Make sure there is no stdin required and catch result
    stdout, stderr = proc.communicate()

    # Check stdout for a values to pick up
    match = re.search('^__VALUES__ = (.*)$', stdout, re.MULTILINE)

    if match is not None:
        values = json.loads(match.group(1))
    else:
        values = None

    # Format return results
    return {
        "command": command,
        "stdout": stdout,
        "stderr": stderr,
        "return_code": proc.returncode,
        "values": values
    }



