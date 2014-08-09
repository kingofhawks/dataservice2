'''
Created on 2013-5-7

@author: YUWANG
'''

from django.conf.urls import *

urlpatterns = patterns('transactionBillManagement.views',
                       (r'bill/$','billIndex'),
                       (r'bill/search$','search'),
                       (r'bill/search/[a-z]+\d+$','accountBillList'),
                       )