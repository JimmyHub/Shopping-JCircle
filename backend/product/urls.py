from django.urls import path
from . import views

urlpatterns=[
    # path('/<str:keyword>/<str:personal>', views.products),
    path('/<str:keyword>/<str:pattern>/<str:personal>/<str:record>', views.ProductView.as_view()),

    # path('/<str:keyword>',views.ProductUPView.as_view()),
    # path('/<str:keyword>/<str:pattern>/<str:personal>/<str:record>', views.products),
    path('/<str:keyword>/photo',views.ProductPhoto.as_view()),
]