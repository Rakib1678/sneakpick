from django.shortcuts import render
from .models import DiscountCode


def apply_discount(request):
    """
    Display all available discount codes for the user.

    This view fetches all discount codes from the database and 
    renders them in the 'apply_discount.html' template. The discount 
    codes can be used by the user during checkout or promotional 
    offers.

    Args:
        request (HttpRequest): The HTTP request object containing user 
        and session data.

    Returns:
        HttpResponse: The rendered HTML response displaying the 
        available discount codes.

    Context:
        - `discount_codes` (QuerySet): A list of all discount codes in 
          the database.
    """
    discount_codes = DiscountCode.objects.all()
    return render(
        request, 
        'promotions/apply_discount.html', 
        {'discount_codes': discount_codes}
    )
