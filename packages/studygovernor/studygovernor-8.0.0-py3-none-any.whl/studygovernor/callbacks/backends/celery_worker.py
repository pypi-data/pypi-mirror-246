from os import environ
from .celery_backend import make_celery

config = {
    'STUDYGOV_CELERY_BACKEND': environ['STUDYGOV_CELERY_BACKEND'],
    'STUDYGOV_CELERY_BROKER': environ['STUDYGOV_CELERY_BROKER'],
}
print('Setting up Celery!!')
celery, task, cron_task = make_celery(config)
print('celery conf:')
for conf in celery.conf:
    print(f'  {conf}')
