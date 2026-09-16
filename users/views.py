from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Wishlist
from products.models import Product
from django.http import HttpResponse
from users.models import Reviews
from django.urls import reverse
import json

def login_view(request):
    """
    Handles user login.

    If the request method is POST, it validates the authentication form and logs in the user.
    If a 'next' parameter exists in the POST data, the user is redirected to the specified URL.
    Otherwise, the user is redirected to the profile page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the login page with the authentication form if the method is GET
                      or the form is invalid. Redirects to another page if the user is successfully logged in.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:            
                return redirect('users:profile')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """
    Handles user logout.

    Logs out the user when the request method is POST and redirects to the login page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Redirects to the login page.
    """
    if request.method == 'POST':
        logout(request)
        return redirect('users:login') 

def signup_view(request):
    """
    Handles user signup.

    If the request method is POST, validates the user creation form and registers the user.
    Logs the user in after successful registration and redirects to the login page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the signup page with the user creation form if the method is GET
                      or the form is invalid. Redirects to another page if the user is successfully registered.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST) 

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:login')
    else:
        form = SignupForm()

    return render(request, 'users/signup.html', {'form':form})

@login_required
def profile_view(request):
    """
    Renders the profile page with user information and wishlist details.

    Retrieves all products and the current user's wishlist to display on the profile page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the profile page with the user, products, and wishlist context.
    """
    user = request.user
    products = Product.objects.all()
    wishlist = Wishlist.objects.filter(user=user)

    return render(request, 'users/profile.html', {
        'user': user,
        'products': products,
        'wishlist': wishlist,
    })

@login_required
def add_to_wishlist(request):
    """
    Adds a product to the user's wishlist.

    Expects a POST request with JSON data containing 'product_id'.
    Creates a new wishlist entry for the user and product if it doesn't already exist.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: A JSON response indicating the product has been added to the wishlist.
    """
    if request.method == 'POST':
        product_id = request.POST.get('product_id')  # ✅ reads from form, not JSON
        product = get_object_or_404(Product, id=product_id)
        
        Wishlist.objects.get_or_create(user=request.user, product=product)

        return redirect('users:profile')  # ✅ sends user to their profile or wishlist page

@login_required
def remove_from_wishlist(request):
    """
    Removes a product from the user's wishlist.

    Expects a POST request with JSON data containing 'product_id'.
    Deletes the corresponding wishlist entry for the user and product.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: A JSON response indicating the product has been removed from the wishlist.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')

        Wishlist.objects.filter(user=request.user, product_id=product_id).delete()

        return JsonResponse({'message': 'Product removed from wishlist'})
    
   
@login_required(login_url= 'users:login')
def create_review(request, product_id):
    """
 View function to handle the creation of a product review.

    This view allows users to submit a review and rating for a specific product. It validates the 
    review text and rating value from the POST request. The rating is checked to ensure it is an 
    integer between 1 and 5, and the review text cannot be empty. If the review is valid, a new 
    review is created and saved. The product's average rating is optionally updated. If successful, 
    the user is redirected to the product detail page. If the form is invalid or if any validation 
    errors occur, an appropriate error message is returned.

    Args:
        request (HttpRequest): The HTTP request object containing the review form data (review text and rating).
        product_id (int): The ID of the product for which the review is being created.
    
    Returns:
        HttpResponse: A redirect to the product detail page if the review is successfully submitted.
        If there are validation errors, an HTTP response with an error message is returned.
    
    Raises:
        Http404: If no product with the given `product_id` exists, a 404 error will be raised.

    """
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Get review text and rating from the POST request
        review_text = request.POST.get('review')
        rating_value = request.POST.get('rating')

        if not review_text or not rating_value:
            return HttpResponse("Review and rating cannot be empty.", status=400)

        try:
            # Convert rating to integer
            rating_value = int(rating_value)
            if rating_value < 1 or rating_value > 5:
                raise ValueError("Rating must be between 1 and 5.")
        except ValueError as e:
            return HttpResponse(f"Invalid rating value: {str(e)}", status=400)

        
        review = Reviews(user=request.user, product=product, review=review_text, rating=rating_value)
        review.save()

        
        product.update_rating()

        
        return redirect(reverse('products:product_detail', kwargs={'product_id': product_id}))
    
    
    return render(request, 'users/create_review.html', {'product': product})
