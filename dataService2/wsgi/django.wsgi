import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'dataService2.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
path = '/usr/share/dataService/dataService2/'
if path not in sys.path:
    sys.path.append(path)
