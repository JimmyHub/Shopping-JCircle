from django.urls import path

from . import views
from tools import tokens


urlpatterns=[
    path('/login',tokens.login),
    path('/',views.UsersView.as_view()),
    path('/avatar', views.UserAvatarView.as_view()),

]