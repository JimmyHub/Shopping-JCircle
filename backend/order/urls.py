from django.conf.urls import url
from . import views

urlpatterns=[
   url(r'^/(?P<keyword>\w+)/(?P<mode>\d+)$',views.orders),
   url(r'^/(?P<keyword>\w+)$',views.orders),
   url(r'^/$',views.orders),
]
