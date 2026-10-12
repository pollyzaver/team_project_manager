"""WSGI-конфигурация проекта teamproject."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teamproject.settings")

application = get_wsgi_application()
