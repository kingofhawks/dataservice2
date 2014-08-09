'''
Created on 2013-4-16

@author: YUWANG
'''
from django.conf.urls import *

urlpatterns = patterns('purchaseManagement.views',
                       (r'purchase/$','transactionIndex'),
                       (r'purchase/search$','search'),
                       )