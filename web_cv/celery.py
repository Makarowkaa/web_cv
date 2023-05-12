from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_cv.settings')

app = Celery('web_cv')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.update(
    broker_url=os.environ.get('CELERY_BROKER_URL', 'pyamqp://guest@localhost//'),
    result_backend=os.environ.get('CELERY_RESULT_BACKEND', 'rpc://guest@localhost//'),
    accept_content=['pickle'],
    task_serializer='pickle',
    result_serializer='pickle',
)
