from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin interface for the Cart model."""
    
    list_display = ('user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'user')
    search_fields = ('user__username',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin interface for the CartItem model."""
    
    list_display = ('cart', 'product', 'quantity', 'total_price_display')
    list_filter = ('cart', 'product')
    search_fields = ('cart__user__username', 'product__name')

    def total_price_display(self, obj):
        """Display the total price of the CartItem."""
        return obj.total_price

    total_price_display.short_description = 'Total Price'

