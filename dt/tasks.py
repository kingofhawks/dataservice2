from celery import task
from celery.task import PeriodicTask
from celery.registry import tasks
from datetime import timedelta
from datetime import datetime
from django.core import management    

#Test only
#Deprecated,please see settings.py CELERYBEAT_SCHEDULE
class MyTask(PeriodicTask):
    run_every = timedelta(minutes=1)

    def run(self, **kwargs):
        self.get_logger().info("Time now: " + datetime.now())
        print("Time now: " + datetime.now())

tasks.register(MyTask)

#Test only
@task()
def add(x, y):
    print 'add****'
    return x + y

@task()
def update_index():
    management.call_command('update_index')