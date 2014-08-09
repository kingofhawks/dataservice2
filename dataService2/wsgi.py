# coding=utf-8
"""
WSGI config for dataService2 project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE']='dataService2.settings'

import django.core.handlers.wsgi
application=django.core.handlers.wsgi.WSGIHandler()

path='/usr/share/dataService/dataService2/'
if path not in sys.path:
    sys.path.append(path)
print>>sys.stderr,sys.path
