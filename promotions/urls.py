from django.urls import path
from . import views

app_name = 'promotions'

urlpatterns = [
    path('', views.apply_discount, name='promotions_home'),
    path('apply-discount/', views.apply_discount, name='apply_discount'),
   
]
