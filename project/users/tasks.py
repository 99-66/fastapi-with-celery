import random

import celery
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

# Retry 1. Try/Except Block
# @shared_task(bind=True)
# def task_process_notification(self):
#     try:
#         if not random.choice([0, 1]):
#             raise Exception
#
#         requests.post("https://httpbin.org/delay/5")
#     except Exception as e:
#         logger.error("exception raised,it would be retry after 5 seconds")
#         raise self.retry(exc=e, countdown=5)


# Retry 2. Task Retry Decorator
# @shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 7, "countdown": 5})
# def task_process_notification(self):
#     if not random.choice([0, 1]):
#         raise Exception()
#
#     requests.post("https://httpbin.org/delay/5")


# Retry 3. Exponential Backoff
# @shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5})
# def task_process_notification(self):
#     if not random.choice([0, 1]):
#         raise Exception()
#
#     requests.post("https://httpbin.org/delay/5")


# Retry 4. Task Base Class
class BaseTaskWithRetry(celery.Task):
    autoretry_for = (Exception, KeyError,)
    retry_kwargs = {"max_retries": 5}
    retry_backoff = True


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_process_notification(self):
    if not random.choice([0, 1]):
        raise Exception()

    requests.post("https://httpbin.org/delay/5")


# Celery Signal Handler
# celery task가 실행된 후 호출된다
@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    from project.ws.views import update_celery_task_status
    # celery 는 asyncio를 지원하지 않기 때문에 sync로 사용한다
    async_to_sync(update_celery_task_status)(task_id)

    from project.ws.views import update_celery_task_status_socketio
    update_celery_task_status_socketio(task_id)


@shared_task(name="task_schedule_work")
def task_schedule_work():
    logger.info("task_schedule_work run")


@shared_task(name="default:dynamic_example_one")
def dynamic_example_one():
    logger.info("Example One")


@shared_task(name="low_priority:dynamic_example_two")
def dynamic_example_two():
    logger.info("Example Two")


@shared_task(name="high_priority:dynamic_example_three")
def dynamic_example_three():
    logger.info("Example Three")
