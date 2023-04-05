from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_cv.settings')

app = Celery('web_cv')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.update(
    broker_url='pyamqp://guest:guest@localhost:5672//',
    result_backend='rpc://guest:guest@localhost:5672//',
    accept_content=['pickle'],
    task_serializer='pickle',
    result_serializer='pickle',
)
