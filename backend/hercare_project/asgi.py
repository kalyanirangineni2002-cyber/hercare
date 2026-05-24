"""
ASGI config for hercare_project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hercare_project.settings')
application = get_asgi_application()
