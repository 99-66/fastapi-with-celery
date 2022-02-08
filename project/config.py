import os
import pathlib
from functools import lru_cache

from kombu import Queue


def route_task(name, args, kwargs, options, task=None, **kw):
    if ":" in name:
        queue, _ = name.split(":")
        return {"queue": queue}
    return {"queue": "default"}


class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent

    # Database
    DATABASE_URL: str = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite3")
    DATABASE_CONNECT_DICT: dict = {}

    # Celery
    broker_url: str = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
    result_backend: str = os.environ.get("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")
    beat_schedule: dict = {
        "task-schedule-work": {
            "task": "task_schedule_work",
            "schedule": 5.0    # 5 sec
        }
    }

    task_default_queue: str = "default"
    task_create_missing_queues: bool = False
    task_queues: list = (
        Queue("default"),
        Queue("high_priority"),
        Queue("low_priority"),
    )
    # task_routes = {
    #     "project.users.tasks.*": {
    #         "queue": "high_priority",
    #     }
    # }
    task_routes = (route_task, )

    WS_MESSAGE_QUEUE: str = os.environ.get("WS_MESSAGE_QUEUE", "redis://127.0.0.1:6379/0")


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


@lru_cache
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }

    config_name = os.environ.get("FASTAPI_CONFIG", "development")
    config_cls = config_cls_dict[config_name]

    return config_cls()


settings = get_settings()
