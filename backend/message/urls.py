from django.urls import path
from . import views

urlpatterns = [
    path('/<str:keyword>', views.messages),
]
