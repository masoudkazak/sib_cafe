import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sib_cofe.settings")
celery = Celery("sib_cofe", broker="redis://localhost:6379/2")
celery.config_from_object("django.conf.settings", namespace="CELERY")
celery.autodiscover_tasks()