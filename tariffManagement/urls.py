'''
Created on 2013-3-22

@author: YUWANG
'''
from django.conf.urls import *

urlpatterns = patterns('tariffManagement.views',
                       (r'discount/$','discountsIndex'),
                       (r'discount/addDiscount$','addDiscount'),
                       (r'discount/edit/(\d+)/','editDiscountForm'),
                       (r'discount/edit/editDiscount','editDiscount'),
                       (r'discount/del/(\d+)/','inactiveDiscount'),
                       #
                       (r'package/$','packagesIndex'),
                       (r'package/new$','addPackageForm'),
                       (r'package/addPackage$','addPackage'),
                       (r'package/edit/(\d+)/','editPackageForm'),
                       (r'package/edit/editPackage','editPackage'),
                       (r'package/del/(\d+)/','inactivePackage'),
                       )