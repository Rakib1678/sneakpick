from django.contrib import admin
from .models import ShippingMethod

@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ('method', 'charge', 'estimated_delivery_time', 'is_active')
