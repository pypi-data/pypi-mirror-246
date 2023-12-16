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

from ..util.mail import send_email


def send_mail(callback_execution_data: Dict,
              config: Dict[str, Any],
              subject: str,
              body: str,
              **ignore) -> Dict[str, Any]:
    """
    Send an email with SUBJECT and BODY.

    :param callback_execution_data: All data needed about the callback execution,
    :param config: App configuration,
    :param subject: str,
    :param body: str):
    
    Substitution fields for SUBJECT and BODY are:

       - ``{experiment}``: experiment id
       - ``{experiment_url}``: full url for an experiment
       - ``{action_url}``: full url for an action.


    Example:

    .. code-block:: YAML

      function: send_mail
      callback_arguments:
        subject: Test mail for {experiment}
        body: The email body, this is about {experiment} located at {experiment_url}



    Result of the callback is:

    ==================== ====== ===================================================================
    Variable name        Type   Description
    ==================== ====== ===================================================================
    sender               str    sender used when sending email
    recipient            str    recipient(s) used when sending the email
    subject              str    subject used when sending email, with the fields substituted
    body                 str    the body used when sending email, with the fields substituted
    ==================== ====== ===================================================================
    """
    experiment = callback_execution_data['experiment']
    action = callback_execution_data['action']

    subject = subject.format(
        experiment=experiment['label'],
        experiment_url=experiment['web_uri'],
        experiment_api_url=experiment['api_uri'],
        action_url=action['web_uri'],
        action_api_url=action['api_uri']
    )

    body = body.format(
        experiment=experiment['label'],
        experiment_url=experiment['web_uri'],
        experiment_api_url=experiment['api_uri'],
        action_url=action['web_uri'],
        action_api_url=action['api_uri']
    )

    result = send_email(subject, body)
    print(f"Email sent successfully: "
          f"FROM: {result['sender']},"
          f"TO: {result['recipient']},"
          f"SUBJECT: {result['subject']},"
          f"BODY:\n{result['body']}")

    return result
