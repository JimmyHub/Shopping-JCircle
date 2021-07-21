from . import views
from django.conf.urls import url

urlpatterns=[
     url(r'^/$',views.shoppingcarts),
     url(r'^/(?P<keyword>\w+)$',views.shoppingcarts),
     url(r'^/(?P<keyword>\w+)/delete$',views.shoppingcarts),
]