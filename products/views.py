from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product
from users.models import Reviews


def searchResult(request):
    """
    Handle product search queries and return matching results.

    This view performs keyword-based searching across multiple fields:
    - name
    - brand
    - product_type

    It also supports sorting the results by:
    - name (alphabetical)
    - price
    - rating

    Parameters
    ----------
    request : HttpRequest
        The incoming HTTP GET request containing:
        - q : str, optional
            The search keyword.
        - sort_by : str, optional
            Field to sort by ('name', 'price', 'rating'). Defaults to 'name'.
        - sort_order : str, optional
            Sorting direction ('asc' or 'desc'). Defaults to 'asc'.

    Returns
    -------
    HttpResponse
        Renders the search results page with the context:
        - query : str
        - results : QuerySet
        - sort_by : str
        - sort_order : str

    Notes
    -----
    If no query is provided, an empty result set is returned.
    """
    query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort_by', 'name')  # default sort 'name'
    sort_order = request.GET.get('sort_order', 'asc')  # default sort ascending

    if query:
        results = Product.objects.filter(
            Q(name__icontains=query)
            | Q(brand__icontains=query)
            | Q(product_type__icontains=query)
        )
    else:
        results = Product.objects.none()

    if sort_by == 'name':
        if sort_order == 'asc':
            results = results.order_by('name')
        else:
            results = results.order_by('-name')
    elif sort_by == 'price':
        if sort_order == 'asc':
            results = results.order_by('price')
        else:
            results = results.order_by('-price')
    elif sort_by == 'rating':
        if sort_order == 'asc':
            results = results.order_by('rating')
        else:
            results = results.order_by('-rating')

    context = {
        'query': query,
        'results': results,
        'sort_by': sort_by,
        'sort_order': sort_order,
    }
    return render(request, 'products/search_results.html', context)


def product_list(request):
    """
    Display a list of products filtered by query parameters.

    This view performs field-based filtering using GET parameters.
    Each filter is optional, and multiple filters can be combined.

    Supported filter fields
    -----------------------
    - name : str
    - brand : str
    - product_type : str
    - size : str
    - color : str
    - year_of_manufacture : int/str
    - price : float/str
    - rating : float/str
    - image : str

    Parameters
    ----------
    request : HttpRequest
        The HTTP request containing optional filter parameters.

    Returns
    -------
    HttpResponse
        Renders the product list page with:
        - products : QuerySet
            The filtered list of products.

    Notes
    -----
    - If no filters are provided, all products are returned.
    - Numeric fields (price, year_of_manufacture, rating) are matched exactly.
    - Text fields use case-insensitive partial matching (icontains).
    """
    filters = {
        'name': request.GET.get('name'),
        'brand': request.GET.get('brand'),
        'product_type': request.GET.get('product_type'),
        'size': request.GET.get('size'),
        'color': request.GET.get('color'),
        'year_of_manufacture': request.GET.get('year_of_manufacture'),
        'price': request.GET.get('price'),
        'rating': request.GET.get('rating'),
        'image': request.GET.get('image'),
    }

    products = Product.objects.all()

    for field, value in filters.items():
        if value:
            if field in ['price', 'year_of_manufacture', 'rating']:
                try:
                    products = products.filter(**{f'{field}__exact': float(value)})
                except ValueError:
                    # Ignore invalid numeric values and continue with other filters
                    continue
            else:
                products = products.filter(**{f'{field}__icontains': value})

    context = {'products': products}
    return render(request, 'products/product_list.html', context)


@login_required(login_url='users:login')
def rate_product(request, product_id):
    """
    Handle user-submitted product ratings.

    This view allows authenticated users to submit a rating for a product.
    The rating is validated and applied using the model's ``set_rating`` method.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request containing POST data with a 'rating' value.
    product_id : int
        The ID of the product being rated.

    Returns
    -------
    HttpResponse
        - Redirects to the product detail page on success.
        - Renders the rating form again with an error message on failure.

    Raises
    ------
    Http404
        If the product with the given ID does not exist.

    Notes
    -----
    - Only logged-in users can submit ratings.
    - ValidationError raised by ``set_rating`` is caught and shown to the user.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            # Get the rating value from the form data
            rating_value = float(request.POST.get('rating'))
            product.set_rating(request.user, rating_value)  # Call the set_rating method
            return redirect('product_detail', product_id=product.id)  # Redirect to product detail page
        except ValidationError as e:
            return render(
                request,
                'products/rate_product.html',
                {'product': product, 'error': str(e)},
            )

    return render(request, 'products/rate_product.html', {'product': product})


def product_detail(request, product_id):
    """
    Display detailed information for a single product and its reviews.

    This view retrieves a product by ID and fetches all related reviews.
    Both the product and its reviews are passed to the template.

    Parameters
    ----------
    request : HttpRequest
        The incoming HTTP request.
    product_id : int
        The ID of the product to display.

    Returns
    -------
    HttpResponse
        Renders the product detail page with:
        - product : Product
        - reviews : QuerySet

    Raises
    ------
    Http404
        If the product with the given ID does not exist.
    """
    product = get_object_or_404(Product, id=product_id)
    reviews = Reviews.objects.filter(product=product)  # Get all reviews for this product
    return render(request, 'products/product_detail.html', {'product': product, 'reviews': reviews})