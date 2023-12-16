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

from typing import Dict, Any
import time


def sleep(callback_execution_data: Dict,
          config: Dict[str, Any],
          seconds: int,
          **kwargs) -> Dict[str, Any]:
    """
    Simple callback that just sleeps for a number of seconds

    :param callback_execution_data:
    :param config:
    :param seconds: How many seconds to sleep
    :param kwargs: Extra arguments are added in the return value
    :return:

    Example:

    .. code-block:: YAML

      function: sleep
      callback_arguments:
        seconds: 10
        kwargs:
          extra_random_argument: 42

    ``kwargs`` can contain any nested data. It will simply be return by the callback. This is meant for
    either debug purposes or to inject extra variables.

    Result of the callback are:

    ==================== ====== ===================================================================
    Variable name        Type   Description
    ==================== ====== ===================================================================
    sleep_duration       int    How long the callback slept for
    extra_kwargs         dict   The values supplied to ``kwargs`` are returned here
    ==================== ====== ===================================================================

    """
    print(f"Going to sleep for {seconds} seconds")
    time.sleep(seconds)
    print("Waking up")

    return {
        "sleep_duration": seconds,
        "extra_kwargs": kwargs,
    }
