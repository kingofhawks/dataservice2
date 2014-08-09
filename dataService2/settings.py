# Django settings for dataService2 project.
# coding=utf-8
import os
import sys

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'DSCPDB',  # Or path to database file if using sqlite3.
        'USER': 'root',  # Not used with sqlite3.
        'PASSWORD': 'abc123',  # Not used with sqlite3.
        'HOST': '192.168.0.213',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
# TIME_ZONE = 'America/Chicago'
# TIME_ZONE = 'Asia/Shanghai' #chuzhen
TIME_ZONE = 'Etc/GMT-8'  # chuzhen

# SESSION_ENGINE # chuzhen
SESSION_COOKIE_AGE = 60 * 24  # chuzhen

# MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'  # chuzhen
# MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'  # chuzhen
MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'  # chuzhen

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #'/usr/share/dataService/dataService2/dataService2/static',  # chuzhen
    'E:/workspace/dataService2/dataService2/static',  # wxp
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'django.template.loaders.filesystem.load_template_source',  # chuzhen
    'django.template.loaders.app_directories.load_template_source',  # chuzhen

)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0av=up&amp;+$6kg_%jf!1h$)1ibpjghkpe)t-uv(r_6^izs!k=&amp;37'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

ROOT_URLCONF = 'dataService2.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'dataService2.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #'/usr/share/dataService/dataService2/dataService2/templates',  # chuzhen
    'E:/workspace/dataService2/dataService2/templates',  # wxp
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (# chuzhen
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'testapp',  # chuzhen
    'my',  # chuzhen
    'vh',  # chuzhen
    'cs',  # chuzhen
    'dt',
    'django_tables2',
    'crispy_forms',
    'haystack',
    'djcelery',
    'db',
    'login',
    'usersManagement',
    'messagesManagement',
    'productManagement',
    'tariffManagement',
    'purchaseManagement',
    'transactionBillManagement',
    'sysAdminManagement',
    'tastypie',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

'''
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
'''
LOGGING = {  # chuzhen
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format':'%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelno)d:%(levelname)s]- %(message)s'
        },
        'verbose': {
            'format':'%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'concise_operate':{
            'format':'%(asctime)s[%(lineno)d][%(levelno)d]:%(message)s'
        },
        'db_format': {
            'format':'%(asctime)s [%(name)s:%(lineno)d] [%(levelno)d:%(levelname)s]- %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            # 'filename':'/usr/share/dataService/dataService2/dataService2/logs/request.log',
            'filename':'/tmp/dscp_request.log',
            'formatter':'standard',
        },
        'db_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            # 'filename':'/usr/share/dataService/dataService2/dataService2/logs/db.log',
            'filename':'/tmp/dscp_db.log',
            'formatter':'db_format',
            'maxBytes':1024 * 1024 * 1,  # 1 MB
            'backupCount':5,
        },
        'operate_handler': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            # 'filename':'/usr/share/dataService/dataService2/dataService2/logs/operate.log',
            'filename':'/tmp/dscp_operate.log',
            'formatter':'concise_operate',
        },
    },
    'loggers': {
        'django.request': {
            'handlers':['request_handler'],
            'level':'DEBUG',
            'propagate':True,
        },
        'django.db.backends': {
            'handlers':['db_handler'],
            'level':'DEBUG',
        },
        'operate': {
            'handlers': ['operate_handler'],
            'level': 'INFO',
        },
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}
#
#
#
#
#
import djcelery
djcelery.setup_loader()
#MongoDB broker
#BROKER_URL = 'amqp://guest:guest@localhost:5672/'
#Redis broker
BROKER_URL = 'redis://192.168.106.109:6379/0'
#CELERY_IMPORTS = ('dt.tasks', )

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    # Update haystack search engine index
    'update-search-engine-index': {
        'task': 'dt.tasks.update_index',
        'schedule': crontab(minute='*/1'),
        'args': (),
    },
}
