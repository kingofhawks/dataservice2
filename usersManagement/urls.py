'''
Created on 2013-1-21

@author: YUWANG
'''
from django.conf.urls import *


urlpatterns = patterns('usersManagement.views',
                       (r'customer/$','customerIndex'),
                       (r'customer/edit$','addCustomerForm'),
                       (r'customer/detail/[a-zA-Z]+\d+$','customerDetail'),
                       #(r'customerManagement/addCustomer$','addCustomer'),
                       (r'customer/edit/[a-zA-Z]+\d+$','EditCustomerForm'),
                       (r'customer/editCustomer$','editCustomer'),
                       (r'customer/del/[a-zA-Z]+\d+$','delCustomer'),                       
                       (r'customer/accountList/[a-zA-Z]+\d+$','accountIndex'),
                      # (r'customer/accountList/cancelAccount$','cancelAccount'),
                       
                       (r'customerGroups/$','customerGroupsIndex'),                       
                       (r'customerGroups/edit/(\d+)/','editCustomerGroupForm'),
                       (r'customerGroups/edit/editCustomerGroup$','editCustomerGroup'),
                       (r'customerGroups/new/$','addCustomerGroupForm'),
                       (r'customerGroups/addCustomerGroup$','addCustomerGroup'),
                       )