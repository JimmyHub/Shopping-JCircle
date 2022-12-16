from django.urls import path

from . import views
urlpatterns = [
    path('/', views.OrdersViewSet.as_view({'post': 'create'})),
    path('/<str:pk>', views.OrdersViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy'})),
    path('/<str:keyword>/<str:mode>', views.OrdersViewSet.as_view({'get': 'list'})),
]

