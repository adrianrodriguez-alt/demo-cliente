import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__SLUG__.settings")
application = get_wsgi_application()
