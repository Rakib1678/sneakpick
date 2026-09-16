# from django.contrib import admin
# from django.urls import path, include
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.conf.urls.static import static
# from django.conf import settings
# from home.views import homepage

# urlpatterns = [
#     path('', include('home.urls')),
#     path('admin/', admin.site.urls),
#     path('users/', include('users.urls')),
#     path('products/', include('products.urls')),
#     path('Orders/',include('orders.urls') ),
#     path('shipping/', include('shipping.urls')),
#     path('promotions/', include('promotions.urls')),
#     path('cart/', include('cart.urls')),
#     path('payment/', include('payment.urls')),   
# ]

# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('Orders/', include('orders.urls', namespace="orders")),       # ✅ fixed
    path('shipping/', include('shipping.urls', namespace="shipping")), # ✅ fixed
    path('promotions/', include('promotions.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)