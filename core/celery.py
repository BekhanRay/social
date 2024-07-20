from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')

celery_app = Celery('core')

celery_app.config_from_object('core.settings.base', namespace='CELERY')

celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



