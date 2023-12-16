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
import logging
import traceback

from typing import Mapping, Sequence, Dict, Any

from . import replace_mapping


def python_function(callback_execution_data,
                    config: Dict[str, Any],
                    package: str,
                    module: str,
                    function: str,
                    pass_callback_data: bool = True,
                    args: Sequence[str] = None,
                    kwargs: Mapping[str, str] = None,
                    **ignore) -> Dict[str, Any]:
    """
    Calls a python funciton. The function should return a dictionairy.

    :param callback_execution_data: callback execution data
    :param config: flask app configuration dict
    :param package: package that gets imported
    :param module: module that gets loaded
    :param function: function that gets called
    :param pass_callback_data: flag that indicates whether or not the `callback_execution_data` and `config`
           have to be given to the `function` as the first arguments
    :param args: list of args [val1 val2 ...]
    :param kwargs: mapping of keyword arguments {key1: val1, key2: val2}

    The items in args and values in kwargs that contain certain VARS will be replaced. Accepted VARS:

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
        package: os
        module: path
        function: join
        args:
          - $SUBJECT
          - $EXPERIMENT

    Result of the callback is:

    ==================== ====== ===================================================================
    Variable name        Type   Description
    ==================== ====== ===================================================================
    package              str    package where function resides in
    module               str    name of module where function resides in
    function             str    name of the function to run
    args                 list   list of arguments used to call function
    kwargs               dict   list of keyword arguments used to call the function
    return_value         any    return value of the function that was called
    __traceback__        str    in case of an error, the traceback as a string
    __exception__        str    in case of an error, the error message
    __success__          bool   a boolean that indicates if the function was successful
    ==================== ====== ===================================================================

    """
    args = args or []
    kwargs = kwargs or {}

    logging.debug(f"Starting callback for callback execution: {callback_execution_data['uri']}")

    # Define replacements available
    replacements = {
        # "$XNAT": xnat_uri,
        "$EXPERIMENT": callback_execution_data['experiment']['api_uri'],
        "$SUBJECT": callback_execution_data['subject']['api_uri'],
        "$CALLBACK_EXECUTION": callback_execution_data['api_uri'],
        "$CALLBACK_SECRET": callback_execution_data['secret'],
    }

    # Substitute variables in arguments
    args = [replace_mapping(x, replacements) for x in args]
    kwargs = {k: replace_mapping(v, replacements) for k, v in kwargs.items()}

    # Import function from package/module
    python_function_module = importlib.import_module('.{}'.format(module), package)
    python_function = getattr(python_function_module, function)

    logging.info('Calling function: {}'.format(python_function))

    # Placeholders to put error information
    error = None
    traceback_str = None

    try:
        if pass_callback_data:
            result = python_function(callback_execution_data, config, *args, **kwargs)
        else:
            result = python_function(*args, **kwargs)

    except BaseException as exception:
        error = f'Exception occurred when executing function: {str(exception)}'
        traceback_str = traceback.format_exc()
        logging.error(error)
        result = None
    else:
        logging.debug(f'Finished python_function callback with result: {result}')

        if not check_json_serializable(result):
            error = f"Cannot serialise result to JSON, cannot store result! Result value: {result}"
            logging.warning(error)
            result = None

    return {
        "package": package,
        "module": module,
        "function": function,
        "args": args,
        "kwargs": kwargs,
        "return_value": result,
        "__traceback__": traceback_str,
        "__exception__": error,
        "__success__": not bool(error),
    }


def check_json_serializable(data: Any) -> bool:
    """
    Check if data is serializable
    :param data:
    :return:
    """
    if not isinstance(data, (bool, str, int, float, type(None), list, tuple, dict)):
        return False

    if isinstance(data, (list, tuple)):
        for element in data:
            if not check_json_serializable(element):
                return False

    if isinstance(data, dict):
        for key, value in data.items():
            if not isinstance(key, str):
                return False

            if not check_json_serializable(value):
                return False

    return True
