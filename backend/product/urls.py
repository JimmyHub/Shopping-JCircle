from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^/(?P<keyword>[\w]{1,11})/(?P<personal>\d+)$',views.products),
    url(r'^/(?P<keyword>[\w]{1,11})/(?P<personal>\d+)/(?P<key1>\d+)/(?P<key2>\d+)/(?P<key3>\d+)$',views.products),
    url(r'^/(?P<keyword>[\w]{1,11})/delete$',views.products),
    url(r'^/(?P<keyword>\w+)/photo$',views.products_photo),
]

