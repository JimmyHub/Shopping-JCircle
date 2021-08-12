from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^/(?P<keyword>[\w]+)/(?P<personal>\d+)$',views.products),
    url(r'^/(?P<keyword>[\w]{1,11})/(?P<pattern>\w+)/(?P<personal>\d+)/(?P<record>\w*&?\w*&?\w*)$',views.products),
    url(r'^/(?P<keyword>\w+)/photo$',views.products_photo),
]

