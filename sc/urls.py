# coding=utf-8
from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    (r'^$', views.index),
    (r'^index/$', views.index),
)
#
#
#
#
#
