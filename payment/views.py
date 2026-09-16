

from decimal import Decimal, InvalidOperation
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from orders.models import Order
from .models import Payment, BankAccount


@login_required(login_url='users:login')
def payment(request):
    """
    Payment method selection screen.
    Just renders the template where user chooses Bank Transfer, etc.
    """
    return render(request, "payment/payment.html")


@require_http_methods(["GET", "POST"])
@login_required(login_url='users:login')
def payment_details(request):
    """
    Payment details form (popup).
    Handles both GET (show form) and POST (process payment).
    """
    if request.method == "GET":
        order_id = request.GET.get("order_id")
        amount = request.GET.get("amount")
        payment_method = request.GET.get("payment_method")

        if not order_id or not amount:
            return JsonResponse({"status": "error", "errors": "Missing fields: order_id, amount"})

        return render(request, "payment/payment_details.html", {
            "order_id": order_id,
            "amount": amount,
            "payment_method": payment_method,
        })

    # POST: process payment
    order_id = request.POST.get("order_id")
    payment_method = request.POST.get("payment_method")
    account_number = request.POST.get("account_number")
    password = request.POST.get("password")
    amount_str = request.POST.get("amount")

    # Validate required fields
    missing = [
        key for key, val in {
            "order_id": order_id,
            "payment_method": payment_method,
            "account_number": account_number,
            "password": password,
            "amount": amount_str,
        }.items() if not val
    ]
    if missing:
        return JsonResponse(
            {"status": "error", "errors": f"Missing fields: {', '.join(missing)}"},
            status=400,
        )

    # Parse amount
    try:
        amount = Decimal(amount_str)
        if amount <= 0:
            raise InvalidOperation
    except (InvalidOperation, TypeError):
        return JsonResponse({"status": "error", "errors": "Invalid amount."}, status=400)

    # Get order
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != "Pending":
        return JsonResponse(
            {"status": "error", "errors": f"Order status must be Pending. Current: {order.status}"},
            status=400,
        )

    # Get account
    try:
        account = BankAccount.objects.get(account_number=account_number, user=request.user)
    except BankAccount.DoesNotExist:
        return JsonResponse({"status": "error", "errors": "Account not found."}, status=404)

    if not account.check_password(password):
        return JsonResponse({"status": "error", "errors": "Incorrect password."}, status=401)

    if account.balance < amount:
        return JsonResponse({"status": "error", "errors": "Insufficient funds."}, status=402)

    # Deduct balance
    account.balance -= amount
    account.save()

    # Create or update payment
    payment_obj, _ = Payment.objects.get_or_create(
        order=order,
        defaults={
            "user": request.user,
            "amount": amount,
            "method": payment_method,
            "status": "Pending",
        },
    )
    payment_obj.amount = amount
    payment_obj.method = payment_method
    payment_obj.status = "Completed"
    payment_obj.save()

    # Update order
    order.payment_status = "Paid"
    order.status = "Confirmed"
    order.save()

    return JsonResponse(
        {
            "status": "success",
            "message": "Payment completed successfully.",
            "order_id": order.id,
            "payment_id": payment_obj.id,
        },
        status=200,
    )