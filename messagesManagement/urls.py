'''
Created on 2013-1-31

@author: YUWANG
'''
from django.conf.urls import *

urlpatterns = patterns('messagesManagement.views',
                       (r'^$','messagesIndex'),
                       (r'send$','MessageForm'),
                       )