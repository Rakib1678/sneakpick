from django.contrib import admin
from .models import Payment, BankAccount



@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    """
    Admin interface for the BankAccount model.

    Automatically hashes the password when saving a new or updated account.
    """

    list_display = ("id", "user", "account_number", "balance")
    search_fields = ("account_number", "user__username")
    list_filter = ("user",)
    fields = ("user", "account_number", "password", "balance")

    def save_model(self, request, obj, form, change):
        raw_password = form.cleaned_data.get("password")
        if raw_password:
            obj.set_password(raw_password)
        super().save_model(request, obj, form, change)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Admin interface for the Payment model.

    Provides management of payments linked to orders, including amount,
    method, status, and transaction details.
    """

    list_display = (
        "id",
        "user",
        "order",
        "amount",
        "method",
        "status",
        "payment_date",
        "transaction_id",
    )
    list_filter = ("status", "method", "payment_date")
    search_fields = ("user__username", "order__id", "transaction_id")