from django.urls import path
from . import views

urlpatterns = [
    path('/<str:keyword>/<str:pattern>/<str:personal>/<str:record>',
         views.ProductViewSet.as_view({'get': 'list'})),
    path('/', views.ProductViewSet.as_view({'post': 'create'})),
    path('/<int:pk>', views.ProductViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy'})),
    # photo 的部分待處理
    path('/<str:keyword>/photo', views.ProductPhoto.as_view()),
]
