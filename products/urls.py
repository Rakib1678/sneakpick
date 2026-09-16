from django.urls import path
from .views import searchResult
from . import views
from .views import product_list

app_name="products"

urlpatterns = [
    path('', product_list, name='product_list'),
    path('search/', searchResult, name='search'),
    path('filter/', product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/rate/', views.rate_product, name='rate_product'),
]
