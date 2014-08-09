# coding=utf-8
from django.conf.urls import patterns, include, url
import views
from api import DataResource
from tastypie.api import Api

#data_resource = DataResource()
v1_api = Api(api_name='v1')
v1_api.register(DataResource())

urlpatterns = patterns('',
    (r'^$', views.index),
    (r'^data/$', views.data_list),   
    (r'^mypublish/$', views.my_publish),
    (r'^publish/$', views.publish),
    (r'^mydata/$', views.my_data),
    (r'^subscribe/$', views.subsribe),
    (r'^trade/$', views.data_trade),
    (r'^download/$', views.download),
    (r'^download2cloud/$', views.download_cloudstorage),
    url('detail/(\d+)/', views.data_detail, name='data_detail'),
    #(r'^api/', include(data_resource.urls)),
    (r'^apikey/', views.api_key),
    (r'^api/', include(v1_api.urls)),
    
)
#
#
#
#
#
