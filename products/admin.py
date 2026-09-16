from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'product_type', 'size', 'color', 'year_of_manufacture', 'price', 'rating', 'image')
    search_fields = ('name', 'brand', 'product_type', 'size', 'color')
    list_filter = ('product_type', 'brand', 'year_of_manufacture')
    list_display_links = ('name', 'image')  # Makes name and image clickable in the admin list view
