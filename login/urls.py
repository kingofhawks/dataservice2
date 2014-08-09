'''
Created on 2013-2-21

@author: YUWANG
'''
from django.conf.urls import *
import views

# urlpatterns = patterns('login.views',                       
#                        (r'login$','login'),
#                        (r'^$','framset'),
#                        (r'^left.html','navigation'),                       
#                        )

urlpatterns = patterns('',
    (r'^$', views.index),
    (r'^login$',views.login),
    (r'^framset',views.framset),
    (r'^left',views.navigation),
    (r'^logout',views.logout),
#                        (r'^$','framset'),
#                        (r'^left.html','navigation'), 
#     (r'^data/$', views.data_list),   
#     (r'^mypublish/$', views.my_publish),
#     (r'^publish/$', views.publish),
#     (r'^mydata/$', views.my_data),
#     (r'^subscribe/$', views.subsribe),
#     (r'^trade/$', views.data_trade),
#     (r'^download/$', views.download),
#     (r'^download2cloud/$', views.download_cloudstorage),
#     url('data/(\d+)/', views.data_detail, name='data_detail'),
)