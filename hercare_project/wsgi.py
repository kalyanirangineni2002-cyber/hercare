"""
WSGI config for hercare_project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hercare_project.settings')
application = get_wsgi_application()
