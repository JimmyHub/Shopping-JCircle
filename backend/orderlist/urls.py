from django.urls import path
from . import views

urlpatterns=[
   path('/<int:keyword>/<str:mode>',views.OrderlistView.as_view()),
]