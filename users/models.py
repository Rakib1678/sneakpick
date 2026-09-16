from django.contrib.auth.models import AbstractUser
from django.db import models
from products.models import Product


class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    address = models.TextField()
    payment_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class Wishlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s wishlist item: {self.product}"


class Reviews(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField( blank = False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=0)  # Rating field from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Review" 
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"{self.user}'s review item: {self.product}"

    
