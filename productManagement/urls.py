'''
Created on 2013-3-15

@author: YUWANG
'''


from django.conf.urls import *

urlpatterns = patterns('productManagement.views',
                       #
                       (r'serviceCategory/$','serviceCategorysIndex'),
                       (r'serviceCategory/addServiceCategory$','addServiceCategory'),
                       (r'serviceCategory/edit/(\d+)/','editServiceCategoryForm'),
                       (r'serviceCategory/edit/editServiceCategory$','editServiceCategory'),
                       (r'serviceCategory/del/(\d+)/','deleteServiceCategory'),
                       #
                       (r'productCategory/$','productCategoryIndex'),
                       (r'productCategory/addProductCategory$','addProductCategory'),
                       (r'productCategory/edit/(\d+)/','editProductCategoryForm'),
                       (r'productCategory/edit/editProductCategory$','editProductCategory'),
                       (r'productCategory/del/(\d+)/','deleteProductCategory'),
                       #
                       (r'product/$','productIndex'),
                       (r'product/new$','addProductForm'),
                       (r'product/addProduct$','addProduct'),
                       (r'product/detail/(\d+)/','productDetail'),
                       (r'product/edit/(\d+)/','editProductForm'),
                       (r'product/edit/editProduct$','editProduct'),
                       (r'product/del/(\d+)/','inactiveProduct'),
                       )