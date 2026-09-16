from django.contrib import admin
from .models import DiscountCode

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'discount_percentage', 'valid_from', 'valid_to', 'is_active')
    search_fields = ('code', 'description')
    list_filter = ('is_active', 'valid_from', 'valid_to')
    ordering = ('-valid_from',)  # Sort by valid_from, descending
