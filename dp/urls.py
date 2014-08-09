# coding=utf-8
from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    (r'^$', views.index),
    (r'^index/$', views.index),
    (r'^project/select/$', views.tenant_select),
    (r'^project/select/submit/$', views.tenant_select_submit),
    (r'^history/$', views.data_process_history),
    (r'^(\d+)/detail/$', views.data_process_detail),
    (r'^launch/$', views.data_process_launch),
    (r'^launch/submit/$', views.data_process_launch_submit),
    (r'^collection/cart/$', views.data_collection_cart),
    (r'^collection/set/$', views.data_collection_set),
    (r'^collection/add/$', views.data_collection_add),
    (r'^collection/del/$', views.data_collection_del),
    (r'^collection/clear/$', views.data_collection_clear),
    (r'^collection/(.+)/$', views.container_select),
    (r'^algorithm/cart/$', views.algorithm_cart),
    (r'^algorithm/set/$', views.algorithm_set),
    (r'^algorithm/add/$', views.algorithm_add),
    (r'^algorithm/del/$', views.algorithm_del),
    (r'^algorithm/clear/$', views.algorithm_clear),
    (r'^algorithm/(.+)/$', views.algorithm_select),
    (r'^monitor/(\d+)/$', views.data_process_monitor),
    (r'^monitor/(\d+)/status/$', views.data_process_status),
)