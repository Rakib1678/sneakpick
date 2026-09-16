from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment, name='payment'), 
    path('payment_details/', views.payment_details, name='payment_details'), 
]
