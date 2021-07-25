from . import views
from django.conf.urls import url

urlpatterns=[
     url(r'^/(?P<keyword>\w+)$',views.shoppingcarts),
]