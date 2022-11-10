from . import views
from django.urls import path

urlpatterns=[
     path('/<int:keyword>',views.ShoppingView.as_view()),
]