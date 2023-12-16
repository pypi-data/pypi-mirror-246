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

import os
from .command import command
from typing import Optional, Mapping, Sequence,Dict, Any


def external_program(callback_execution_data,
                     config: Dict[str, Any],
                     binary: str,
                     args: Optional[Sequence[str]] = None,
                     kwargs: Optional[Mapping[str, str]] = None,
                     xnat_external_system_name: str='XNAT',
                     **ignore) -> Dict[str, Any]:
    """
    Calls a binary from the StudyGovernor binaries directory. This is configured using the
    ``STUDYGOV_PROJECT_BIN`` configuration field.

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

    - ``$EXPERIMENT``: will be substituted with the experiment URL.
    - ``$SUBJECT``: will be substituted with the subject URL.
    - ``$XNAT``: will be substituted with the XNAT URL.
    - ``$CALLBACK_EXECUTION``: Will be substituted with the callback execution URL
    - ``$CALLBACK_SECRET``: Will be substituted with the callback execution secret

    Example:

    .. code-block:: YAML

      function: external_program
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
    # Validate the binary is in fact in the binary dir and get full path
    binaries = os.listdir(config['STUDYGOV_PROJECT_BIN'])

    if binary not in binaries:
        raise ValueError('Cannot find binary {} in {}'.format(binary, config['STUDYGOV_PROJECT_BIN']))

    binary = os.path.join(config['STUDYGOV_PROJECT_BIN'], binary)

    return command(
        callback_execution_data=callback_execution_data,
        config=config,
        binary=binary,
        args=args,
        kwargs=kwargs,
        xnat_external_system_name=xnat_external_system_name,
    )
