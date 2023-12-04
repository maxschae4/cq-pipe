import os

from celery import Celery

RABBIT_MQ_URL = os.getenv("RABBIT_MQ_URL")

app = Celery(
    "cq_pipe", broker=RABBIT_MQ_URL, backend="rpc://", include=["cq_pipe.tasks"]
)

app.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    app.start()
