from celery import Celery

url_broker = 'amqp://user:bitnami@doggys_rabbit:5672//'
url_backend = 'redis://:password123@doggys_redis:6379/0'


app = Celery('worker', broker=url_broker, backend=url_backend)


app.conf.task_routes = {
    "celery_app.task.complex_task": {"queue": "hipri"},
}

app.conf.update(
    task_track_started=True, task_serializer="pickle", accept_content=["pickle", "json"]
)
