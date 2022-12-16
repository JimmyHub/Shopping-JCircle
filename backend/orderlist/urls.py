from django.urls import path
from . import views

urlpatterns = [
    path('/', views.OrderlistViewSet.as_view({'post': 'create'})),
    path('/<int:pk>', views.OrderlistViewSet.as_view({'delete': 'destroy'})),
    path('/<int:keyword>/<str:mode>', views.OrderlistViewSet.as_view({'get': 'list'})),
]
