from celery import Celery

app = Celery("cq_pipe", broker="amqp://", backend="rpc://", include=["cq_pipe.tasks"])

app.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    app.start()
