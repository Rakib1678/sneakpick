from django.contrib import admin
from .models import UserProfile, Wishlist, Reviews

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'address', 'payment_info')
    search_fields = ('username', 'email')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'product__name')

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'product', 'rating', 'created_at')
    search_fields = ('user__username', 'product__name')