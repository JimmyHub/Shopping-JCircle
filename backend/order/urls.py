from django.urls import path

from . import views

urlpatterns=[
   path('/<str:keyword>/<str:mode>',views.OrdersView.as_view()),
]
