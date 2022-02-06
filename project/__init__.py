from fastapi import FastAPI

from project.celery_utils import create_celery


def create_app() -> FastAPI:
    app = FastAPI()

    # main.py 에서 celery 인스턴스를 생성하기 위한 변수 할당
    app.celery_app = create_celery()

    # routes
    from project.users import users_router
    app.include_router(users_router)

    @app.get("/")
    async def root():
        return {"message": "Hello world"}

    return app
