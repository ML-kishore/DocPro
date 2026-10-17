from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docpro.settings')

app = Celery('docpro')

app.config_from_object('django.conf:settings',namespace='CELERY')

app.autodiscover_tasks()