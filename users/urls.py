from django.urls import path
from . import views

app_name = 'users'


urlpatterns = [
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/', views.profile_view, name="profile"),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),   # ✅ moved out of "profile/"
    path('remove-from-wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('product/<int:product_id>/review/', views.create_review, name='create_review'),
]