"""
ASGI config for the AIBridge project.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aibridge.settings")

application = get_asgi_application()
