# coding=utf-8
from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    (r'^$', views.index),
    (r'^index/$', views.index),
    (r'^rnta/$', views.real_name_the_authentication),
    (r'^rnta/submit/$', views.rnta_submit),
    (r'^zhxx/$', views.index),
    (r'^grzl/$', views.grzl),
    (r'^fwlb/$', views.fwlb),
    (r'^zybb/$', views.zybb),
    (r'^jygl/$', views.jygl),
    (r'^lscx/$', views.lscx),
    
    (r'^project/list/$', views.tenant_list),
    (r'^project/create/$', views.tenant_create),
    (r'^project/create/submit/$', views.tenant_create_submit),
    (r'^project/delete/$', views.tenant_delete),
    (r'^project/detail/$', views.tenant_detail),
    (r'^project/create/check/$', views.tenant_create_name_check),
    (r'^project/user/edit/$', views.tenant_edit_user),
    (r'^project/user/edit/submit/$', views.tenant_edit_user_submit),
    
    (r'^user/list/$', views.user_list),
    (r'^user/create/$', views.user_create),
    (r'^user/create/submit/$', views.user_create_submit),
    (r'^user/delete/$', views.user_delete),
    (r'^user/detail/$', views.user_detail),
    (r'^user/create/check/$' , views.user_create_name_check),

)
#
#
#
#
#
