from django.urls import path

from . import views

urlpatterns = [
    path('/login', views.LoginViewSet.as_view({'post':'login'})),
    path('/', views.UsersViewSet.as_view({'get': 'get_user', 'post': 'create', 'patch': 'partial_update'})),
    path('/avatar', views.UserAvatarView.as_view({'post': 'create'})),

]
