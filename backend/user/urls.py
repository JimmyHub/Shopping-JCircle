from django.conf.urls import url
from . import views
from tools import tokens
urlpatterns=[
    url(r'^/login$',tokens.login),
    url(r'^/avatar$',views.user_avatar),
    url(r'^/',views.users),
]