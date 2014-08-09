# coding=utf-8
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from test import test1
import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^hello/$', test1.hello),
    (r'^hello2/$', test1.hello2),
    (r'^hello3/$', test1.hello3),
    (r'^hello4/$', test1.hello4),
    (r'^hello5/$', test1.hello5),
    (r'^hello6/$', test1.hello6),
    (r'^searchtest/$', test1.searchtest),
    (r'^contacttest/$', test1.contacttest),
    url(r'^testapp/', include('testapp.urls')),

    url(r'^$', views.index),
    url(r'^index/$', views.index),
    url(r'^login/$', views.login),
    url(r'^regist/$', views.regist),
    url(r'^login_submit/$', views.login_submit),
    url(r'^regist_submit/$', views.regist_submit),
    url(r'^regist_loginName_check/$', views.regist_loginName_check),
    url(r'^regist_email_check/$', views.regist_email_check),
    url(r'^logout/$', views.logout),

    url(r'^my/', include('my.urls')),
    url(r'^virtualHost/', include('vh.urls')),
    url(r'^cloudStorage/', include('cs.urls')),
    url(r'^dataProcessing/', include('dp.urls')),
    url(r'^market/', include('dt.urls')),
    url(r'^pricingStandrd/$', include('ps.urls')),
    url(r'^supportCenter/$', include('sc.urls')),
    (r'^search/', include('haystack.urls')),
    (r'^billing/',include('login.urls')),
    (r'^usersManagement/',include('usersManagement.urls')),
    (r'^my/messages/',include('messagesManagement.urls')),
    (r'productManagement/',include('productManagement.urls')),
    (r'purchaseManagement/',include('purchaseManagement.urls')),
    (r'sysAdminManagement',include('sysAdminManagement.urls')),
    (r'tariffManagement/',include('tariffManagement.urls')),
    (r'transactionBillManagement/',include('transactionBillManagement.urls')),


#    url(r'^',include('default.urls')),
    # Examples:
    # url(r'^$', 'dataService2.views.home', name='home'),
    # url(r'^dataService2/', include('dataService2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
# urlpatterns += staticfiles_urlpatterns()
