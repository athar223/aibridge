"""WSGI entrypoint for Vercel's Python runtime.

Vercel's @vercel/python builder looks for a module-level `app` callable.
Kept separate from aibridge/wsgi.py (used by gunicorn on Render/Railway/
PythonAnywhere) so each platform's entrypoint stays purpose-built.
"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aibridge.settings")

from django.core.wsgi import get_wsgi_application  # noqa: E402

app = get_wsgi_application()
