from . import views
from django.urls import path

urlpatterns = [
    path('/', views.ShoppingViewSet.as_view({'get': 'list'})),
    path('/<int:keyword>', views.ShoppingViewSet.as_view({'post':'create'})),
    path('/<str:pk>', views.ShoppingViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy'}))
]
