# coding=utf-8
from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    (r'^$', views.index),
    (r'^index/$', views.index),
    (r'^project/select/$', views.tenant_select),
    (r'^project/select/submit/$', views.tenant_select_submit),
    (r'^display/$', views.displsy),
    (r'^display/(.+)/$', views.container),
    # (r'^display/(.+[/download/])$', views.download),
    (r'^container/create/$', views.container_create),
    (r'^container/create/submit/$', views.container_create_submit),
    (r'^container/delete/submit/$', views.container_delete_submit),
    (r'^folder/create/$', views.folder_create),
    (r'^folder/create/submit/$', views.folder_create_submit),
    (r'^folder/delete/submit/$', views.folder_delete_submit),
    # (r'^file/upload/$', views.file_upload),
    # (r'^file/upload/submit/$', views.file_upload_submit),
    #(r'^file/download/$', views.file_download),
    (r'^file/delete/submit/$', views.file_delete_submit),
)
#
#
#
#
#
