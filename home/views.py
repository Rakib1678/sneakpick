from django.shortcuts import render
from products.models import Product

# Create your views here.


def homepage(request):
    return render(request, 'home/homepage.html')

def homepage(request):
    featured = Product.objects.all()[:3]  # pick any 3 products
    return render(request, 'home/homepage.html', {'featured': featured})