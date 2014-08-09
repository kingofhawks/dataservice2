# coding=utf-8
from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    (r'^$', views.index),
    (r'^index/$', views.index),
    (r'^project/select/$', views.tenant_select),
    (r'^project/select/submit/$', views.tenant_select_submit),
    (r'^summary/$', views.summary),
    (r'^server/list/$', views.server_list),
    (r'^server/(.{36})/detail/', views.server_detail),
    (r'^server/(.{36})/delete/', views.server_delete),
    (r'^server/(.{36})/createsnapshot/$', views.server_create_snapshot),
    (r'^server/(.{36})/createsnapshot/submit/$', views.server_create_snapshot_submit),
    (r'^server/create/$', views.server_creat),
    (r'^server/create/submit/$', views.server_creat_submit),
    (r'^image/list/$', views.image_list),
    # (r'^image/detail/$', views.image_detail),
    (r'^volume/list/$', views.volume_list),
    (r'^volume/(.{36})/detail/$', views.volume_detail),
    (r'^volume/(.{36})/delete/$', views.volume_delete),
    (r'^volume/(.{36})/createsnapshot/$', views.volume_create_snapshot),
    (r'^volume/(.{36})/createsnapshot/submit/$', views.volume_create_snapshot_submit),
    (r'^volume/(.{36})/deletesnapshot/$', views.volume_delete_snapshot),
    (r'^snapshot/list/$', views.snapshot_list),
    (r'^snapshot/server/(.{36})/delete/$', views.snapshot_server_delete),
    (r'^flavor/list/$', views.flavor_list),
    (r'^access/list/$', views.access_list),
    (r'^access/floating_ip/allocate/$', views.floating_ip_allocate),
    (r'^access/floating_ip/allocate/submit/$', views.floating_ip_allocate_submit),
    (r'^access/floating_ip/deallocates/(.+)/$', views.floating_ip_deallocate),
    (r'^access/floating_ip/associate/$', views.floating_ip_associate),
    (r'^access/floating_ip/associate/submit/$', views.floating_ip_associate_submit),
    (r'^access/floating_ip/unassociate/$', views.floating_ip_unassociate),
    (r'^keypair/list/$', views.keypair_list),
    (r'^security/list/$', views.security_list),
)
#
#
#
#
#
