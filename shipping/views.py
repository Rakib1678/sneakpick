


from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ShippingMethod
from orders.models import Order

PENDING_STATUSES = ["Pending", "Confirmed", "Created", "Paid"]

def _safe_decimal(value, default="0.00"):
    try:
        if isinstance(value, Decimal):
            return value
        return Decimal(str(value))
    except Exception:
        return Decimal(default)

@login_required
def shipping_Methods(request):
    # 1) Resolve order once, store in session; stop relying on query params
    order_id = request.session.get("shipping_order_id")

    if not order_id:
        # Try to resolve from GET (optional), else last active order
        raw_order_id = request.GET.get("order_id")
        order = None

        if raw_order_id:
            try:
                order = get_object_or_404(Order, id=int(raw_order_id), user=request.user)
            except Exception:
                order = None

        if order is None:
            order = (
                Order.objects.filter(user=request.user, status__in=PENDING_STATUSES)
                .order_by("-id")
                .first()
            )

        if order is None:
            return render(request, "shipping/shipping_methods.html", {
                "methods": [],
                "order_id": "",
                "base_total": Decimal("0.00"),
                "initial_shipping_charge": Decimal("0.00"),
                "total_with_shipping": Decimal("0.00"),
                "error": "No active order found. Create an order first from your cart."
            })

        request.session["shipping_order_id"] = order.id
        order_id = order.id
    else:
        order = get_object_or_404(Order, id=int(order_id), user=request.user)

    # 2) Load available methods
    methods = ShippingMethod.objects.filter(is_active=True).order_by("id")
    if not methods.exists():
        return render(request, "shipping/shipping_methods.html", {
            "methods": [],
            "order_id": order.id,
            "base_total": _safe_decimal(getattr(order, "total_amount", getattr(order, "total_price", "0.00"))),
            "initial_shipping_charge": Decimal("0.00"),
            "total_with_shipping": _safe_decimal(getattr(order, "total_amount", getattr(order, "total_price", "0.00"))),
            "error": "No shipping methods available."
        })

    # 3) Compute base totals from the order model (supports total_amount or total_price)
    base_total = _safe_decimal(getattr(order, "total_amount", getattr(order, "total_price", "0.00")))
    initial_shipping_charge = _safe_decimal(methods[0].charge, default="0.00")
    total_with_shipping = base_total + initial_shipping_charge

    # 4) Handle POST submission
    if request.method == "POST":
        method_id = request.POST.get("shipping_method")
        if not method_id:
            return render(request, "shipping/shipping_methods.html", {
                "methods": methods,
                "order_id": order.id,
                "base_total": base_total,
                "initial_shipping_charge": initial_shipping_charge,
                "total_with_shipping": total_with_shipping,
                "error": "Please select a shipping method."
            })

        try:
            shipping_method = get_object_or_404(ShippingMethod, id=int(method_id), is_active=True)
        except Exception:
            return render(request, "shipping/shipping_methods.html", {
                "methods": methods,
                "order_id": order.id,
                "base_total": base_total,
                "initial_shipping_charge": initial_shipping_charge,
                "total_with_shipping": total_with_shipping,
                "error": "Invalid shipping method."
            })

        # 5) Persist shipping selection on the order
        order.shipping_method = shipping_method.method  # or store FK if your model expects it
        order.shipping_charge = _safe_decimal(shipping_method.charge)
        order.estimated_delivery_time = shipping_method.estimated_delivery_time

        if getattr(order, "status", None) in PENDING_STATUSES:
            order.status = "Shipped"

        order.save()

        # 6) Hard redirect to avoid NoReverseMatch (logs show /Orders/ exists)
        return redirect("orders:order_history")

    # 7) Render GET
    return render(request, "shipping/shipping_methods.html", {
        "methods": methods,
        "order_id": order.id,
        "base_total": base_total,
        "initial_shipping_charge": initial_shipping_charge,
        "total_with_shipping": total_with_shipping,
    })