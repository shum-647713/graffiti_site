from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graffiti_site_api.prod_settings')

application = get_wsgi_application()
