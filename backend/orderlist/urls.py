from django.urls import path
from . import views

urlpatterns = [
    path('/', views.OrderlistViewSet.as_view({'post': 'create'})),
    path('/<int:keyword>/<str:mode>', views.OrderlistViewSet.as_view({'get': 'list','delete': 'destroy'})),
]
