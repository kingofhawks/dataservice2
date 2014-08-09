'''
Created on 2013-5-22

@author: YUWANG
'''
from django.conf.urls import *

urlpatterns = patterns('sysAdminManagement.views',
                       (r'adminGroup/$', 'adminGroupsIndex'),
                       (r'adminGroup/addAdminGroup$', 'addAdminGroup'),
                       (r'adminGroup/edit/(\d+)/', 'editAdminGroupForm'),
                       (r'adminGroup/edit/editAdminGroup$', 'editAdminGroup'),
                       (r'adminGroup/del/(\d+)/', 'delAdminGroup'),
                       (r'sysAdmin/$', 'sysAdminIndex'),
                       (r'sysAdmin/addSysAdmin$', 'addSysAdmin'),
                       (r'sysAdmin/edit/(\d+)/', 'editSysAdminForm'),
                       (r'sysAdmin/edit/editSysAdmin', 'editSysAdmin'),
                       (r'sysAdmin/del/(\d+)/', 'delSysAdmin'),
                       )
