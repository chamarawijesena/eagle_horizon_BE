"""
WSGI config for eagle_horizon project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eagle_horizon.settings')

application = get_wsgi_application()
