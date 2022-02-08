from project import create_app

app = create_app()
celery = app.celery_app


# celery auto-reload
def celery_worker():
    from watchgod import run_process
    import subprocess

    # 변경이 감지될 때 호출되는 콜백 함수
    def run_worker():
        subprocess.call(["celery", "-A", "main.celery", "worker", "--loglevel=info", "-Q", "high_priority,default"])

    run_process("./project", run_worker)


if __name__ == '__main__':
    celery_worker()
