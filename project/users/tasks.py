import random

import requests
from asgiref.sync import async_to_sync
from celery import shared_task
from celery.signals import task_postrun
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y


@shared_task
def sample_task(email):
    from project.users.views import api_call

    api_call(email)


@shared_task(bind=True)
def task_process_notification(self):
    try:
        if not random.choice([0, 1]):
            raise Exception

        requests.post("https://httpbin.org/delay/5")
    except Exception as e:
        logger.error("exception raised,it would be retry after 5 seconds")
        raise self.retry(exc=e, countdown=5)


# Celery Signal Handler
# celery task가 실행된 후 호출된다
@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    from project.ws.views import update_celery_task_status
    # celery 는 asyncio를 지원하지 않기 때문에 sync로 사용한다
    async_to_sync(update_celery_task_status)(task_id)
