# from django.http import HttpResponse
from django.shortcuts import render

# def homeView(request):
#    # return HttpResponse('home page')
#    return render(request, 'homepage.html')

# def aboutView(request):
#    # return HttpResponse('about page')
#    return render(request, 'about.html')


def cart(request):
    """redirects to cart.html

    Args:
        request: HTTP GET Request

    Returns:
        render request to template
    """
    return render(request, 'cart/cart.html')