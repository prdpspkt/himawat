import os
import sys

# Add the project directory to the python path
sys.path.insert(0, os.path.dirname(__file__))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'himwat.settings')

# Setup Django
import django
django.setup()

# Import the WSGI application
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
