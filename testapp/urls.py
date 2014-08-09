# coding=utf-8
from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    (r'^in/$', views.testapp),
#    (r'^hello3/$',views.hello3),
)
#
#
#
#
#
