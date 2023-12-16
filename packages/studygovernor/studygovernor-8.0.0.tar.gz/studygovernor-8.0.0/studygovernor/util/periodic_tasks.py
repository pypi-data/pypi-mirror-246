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

import datetime
import logging
from typing import List

from ..models import db, CallbackExecution, CallbackExecutionStatus, CallbackExecutionResult
from .. import control

# Seconds to minutes, make this changable for testing purposes
FACTOR = 60


def check_timeouts():
    run_timeouts = 0
    wait_timeouts = 0

    executions_to_check_run_timeout: List[CallbackExecution] = CallbackExecution.query.filter(
        CallbackExecution.status == CallbackExecutionStatus.running).all()

    logging.info(f'Checking run timeout for {executions_to_check_run_timeout}')
    for execution in executions_to_check_run_timeout:
        # Skip unset (zero) timeouts
        if not execution.callback.run_timeout:
            pass

        start = execution.run_start
        start = start.replace(tzinfo=None)  # Strip tzinfo that e.g. postgresql adds on
        current = datetime.datetime.now()
        logging.info(f'Start time: {start}, current time: {current}')

        runtime = (current - start).total_seconds() / FACTOR
        logging.info(f'Run time: {runtime}, timeout {execution.callback.run_timeout}')
        if runtime > execution.callback.run_timeout:
            run_timeouts += 1
            execution.result = CallbackExecutionResult.timeout
            control.update_callback_execution_state(execution, CallbackExecutionStatus.finished)
            message = f"ERROR: CallbackExecution run timeout at {current} after {runtime} minutes (started at {start})."
            if execution.run_log:
                execution.run_log = f"{execution.result_log}\n{message}"
            else:
                execution.run_log = message

            db.session.commit()
            control.update_state(execution.experiment)

    executions_to_check_wait_timeout: List[CallbackExecution] = CallbackExecution.query.filter(
        CallbackExecution.status == CallbackExecutionStatus.waiting).all()
    logging.info(f'Checking wait timeout for {executions_to_check_wait_timeout}')
    for execution in executions_to_check_wait_timeout:
        # Skip unset (zero) timeouts
        if not execution.callback.wait_timeout:
            pass

        start = execution.wait_start
        start = start.replace(tzinfo=None)  # Strip tzinfo that e.g. postgresql adds on
        current = datetime.datetime.now()
        logging.info(f'Start time: {start}, current time: {current}')

        waittime = (current - start).total_seconds() / FACTOR
        logging.info(f'Wait time: {waittime}, timeout {execution.callback.wait_timeout}')
        if waittime > execution.callback.wait_timeout:
            wait_timeouts += 1
            execution.result = CallbackExecutionResult.timeout
            control.update_callback_execution_state(execution, CallbackExecutionStatus.finished)
            message = f"ERROR: CallbackExecution wait timeout at {current} after {waittime} minutes (started at {start})."
            if execution.result_log:
                execution.result_log = f"{execution.result_log}\n{message}"
            else:
                execution.result_log = message

            db.session.commit()
            control.update_state(execution.experiment)

    return run_timeouts, wait_timeouts
