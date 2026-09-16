

# cart/views.py
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem

@login_required(login_url='users:login')
def add_to_cart(request):
    """
    Add a product to the authenticated user's cart.
    - If the item exists, increase its quantity.
    - If not, create it with the provided quantity (default 1).
    Then redirect to the cart page.
    """
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        # Use the authenticated user directly
        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('cart:render_cart')

    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=400)

@login_required(login_url='users:login')
def render_cart(request):
    """
    Build a structured cart payload the template expects:
    cart.items: [{id, product_name, price, quantity, total_price, product_id}, ...]
    cart.total: number
    """
    # Use the authenticated user directly
    cart, _ = Cart.objects.get_or_create(user=request.user)

    items = []
    for item in cart.items.select_related('product'):
        items.append({
            'id': item.id,
            'product_name': item.product.name,
            'price': item.product.price,
            'quantity': item.quantity,
            'total_price': item.total_price,
            'product_id': item.product.id,
        })

    context = {
        'cart': {
            'items': items,
            'total': cart.total,
        }
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url='users:login')
def update_cart(request):
    if request.method == "POST":
        cart_item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart item not found'}, status=404)

        if action == "increase":
            cart_item.quantity += 1
            cart_item.save()
        elif action == "decrease":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
        elif action == "remove":
            cart_item.delete()
        else:
            return JsonResponse({'success': False, 'error': 'Invalid action'}, status=400)

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid method'}, status=400)
def cart(request):
    """
    Legacy view: redirect to the canonical cart rendering view.
    """
    return redirect('cart:render_cart')



from orders.models import Order  # import your Order model

@login_required(login_url='users:login')
def checkout(request):
    """
    Convert the user's cart into a Pending order.
    """
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # If cart is empty, redirect back
    if not cart.items.exists():
        return redirect('cart:render_cart')

    # Create a new order
    order = Order.objects.create(
        user=request.user,
        status="Pending",            # waiting for payment
        total_amount=cart.total,     # use cart total
        payment_status="Unpaid"      # if your model has this field
    )

    # Optionally: copy cart items into order items if your Order model tracks products
    # for item in cart.items.all():
    #     OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

    # Clear the cart after checkout
    cart.items.all().delete()

    # Redirect to payment page
    return redirect('payment:payment')




from decimal import Decimal
from orders.models import Order, OrderItem
from cart.models import Cart

@login_required(login_url='users:login')
def checkout(request):
    user_profile = request.user  # ✅ Already a UserProfile

    cart, _ = Cart.objects.get_or_create(user=user_profile)

    if not cart.items.exists():
        return redirect('cart:render_cart')

    order = Order.objects.create(
        user=user_profile,
        status="Pending",
        total_amount=Decimal(cart.total),
        shipping_address="Default Address",
        payment_status="Pending"
    )
    return redirect(f"/payment/payment_details/?order_id={order.id}&amount={order.total_amount}")

    for item in cart.items.select_related('product'):
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart.items.all().delete()

    return redirect('payment')