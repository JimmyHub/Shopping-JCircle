from django.conf.urls import url
from . import views

urlpatterns=[
   url(r'^/$',views.orderlists),
   url(r'^/(?P<keyword>\w+)/(?P<mode>\d+)$',views.orderlists),
]