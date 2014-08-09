Installation Instruction:
1. Install Python2.7
http://www.activestate.com/activepython/downloads
2. Install Django from command console
$->pip install Django
3. Install Python MySQL API:
https://pypi.python.org/pypi/MySQL-python/1.2.4
4. Install keystoneclient:
$->pip install python-keystoneclient
5. Create folder: E:/tmp, see dataService2/settings.py
6. change "TEMPLATE_DIRS"/"STATICFILES_DIRS" in dataService2/settings.py
7. [optional]install pycurl(deprecated and sourceforge , it's better to replace it with requests module or httplib2 etc
http://docs.python-requests.org/en/latest/
https://github.com/kennethreitz/requests
8.Install django-tables2 plugin
pip install django-tables2
9.Install django-crispy-forms
pip install --upgrade django-crispy-forms
10. Install ElasticSearch for search engine
http://www.elasticsearch.org/guide/reference/setup/installation/
manage.py rebuild_index: clear index and rebuild it
manage.py update_index: update data index
11. Install pyelasticsearch for ElasticSearch engine
pip install pyelasticsearch  
12. Install haystack for search engine integration
pip install django-haystack
13. Use django-celery for periodical schedule
pip install django-celery
manage.py celery worker
manage.py celery beat -lDEBUG -S djcelery.schedulers.DatabaseScheduler
Please refer to http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#starting-the-scheduler
14. Install redis server
sudo apt-get install redis
or yum install redis
15. Install python redis client as celery broker
pip install redis
16. Generate SQL tables for django models(data/billing module)
manage.py syncdb
17. Billing module: localhost:8000/billing, username/password:admin/123456
18. tastypie for REST API
pip install django-tastypie

You could setup the dependencies as:
pip install -r requrements.txt

JS Frameworks:
1.JQuery for basic JS operations such as AJAX,DOM selector
2.Twitter BootStrap for CSS and style
3.parsley and HTML5 are used for UI constrains

Git Server:
http://192.168.0.211/gitlab/   username/password:gitlab/123456
