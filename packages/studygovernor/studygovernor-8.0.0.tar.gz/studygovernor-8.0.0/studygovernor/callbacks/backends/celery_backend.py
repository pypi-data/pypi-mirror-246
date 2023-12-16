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


import yaml
from flask import current_app
from typing import Dict, Any

from studygovernor import create_app, load_config_from_env
from .. import CALLBACK_BACKENDS, master_callback, clean_config
from ...util.periodic_tasks import check_timeouts

try:
    from celery import Celery, signals
    from celery.signals import worker_process_init
    from celery.schedules import crontab
    CELERY_IMPORTED = True
except ImportError:
    CELERY_IMPORTED = False


def make_celery(config):
    celery = Celery("studygovernor",
                    broker=config['STUDYGOV_CELERY_BROKER'],
                    backend=config['STUDYGOV_CELERY_BACKEND'])

    # Add environment to config
    celery.conf.update(load_config_from_env())

    # Update config values from the app config
    celery.conf.update(config)

    # Celery configuration, set beat schedule
    celery.conf.beat_schedule = {
        # Executes every minute
        'periodic_tasks': {
            'task': 'studygovernor.callbacks.backends.celery_backend.studygovernor_cron',
            'schedule': crontab(minute="*")
        }
    }

    cron_task = celery.task(ignore_result=True)(studygovernor_cron)

    task = celery.task(ignore_result=True,
                       autoretry_for=(Exception,),
                       retry_backoff=5,
                       retry_jitter=True,
                       retry_kwargs={'max_retries': 5})(task_callback)

    return celery, task, cron_task


def studygovernor_cron():
    app = create_app()
    with app.app_context():
        run_timeouts, wait_timeouts = check_timeouts()
        print(f"Found and marked {run_timeouts} run timeouts and {wait_timeouts} wait timeouts.")


def task_callback(*,
                  callback_function: str,
                  callback_arguments: str,
                  callback_execution_url: str,
                  callback_execution_secret: str,
                  config: Dict[str, Any]):
    master_callback(callback_function=callback_function,
                    callback_arguments=callback_arguments,
                    callback_execution_url=callback_execution_url,
                    callback_execution_secret=callback_execution_secret,
                    config=config)


def celery_callback(callback_function: str,
                    callback_arguments: str,
                    callback_execution_url: str,
                    callback_execution_secret: str,
                    config: Dict[str, Any]):
    callback_data_info = yaml.safe_load(callback_arguments)
    callback_queue = callback_data_info.get('queue', 'celery')

    if not CELERY_IMPORTED:
        raise ImportError("Cannot use celery callback, celery python package appears not to be installed!")
    
    celery, task, cron_task = make_celery(dict(config))

    current_app.logger.info(f'Created: {task}')
    current_app.logger.info(f'delay celery callback: {callback_execution_url}')
    current_app.logger.info(f'Using celery callback queue: {callback_queue}')

    apply_kwargs = {
        'callback_function': callback_function,
        'callback_arguments': callback_arguments,
        'callback_execution_url': callback_execution_url,
        'callback_execution_secret': callback_execution_secret,
        'config': config,
    }

    # Use kwargs so the hooks can easily pick up arguments
    result = task.apply_async(
        kwargs=apply_kwargs,
        queue=callback_queue
    )
    current_app.logger.info(f'Delayed task status: {result.status}')


CALLBACK_BACKENDS['celery'] = celery_callback
