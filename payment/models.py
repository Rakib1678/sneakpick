
from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from decimal import Decimal
from orders.models import Order


class BankAccount(models.Model):
    """
    Represents a user's local bank account for payment authentication.

    Attributes
    ----------
    user : User
        The owner of the bank account.
    account_number : str
        Unique identifier for the bank account.
    password : str
        Hashed password used to authenticate payments.
    balance : Decimal
        Current available balance in the account.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bank_accounts",
    )
    account_number = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    def set_password(self, raw_password: str) -> None:
        """
        Hash and set the account password.

        Parameters
        ----------
        raw_password : str
            The plain-text password to hash and store.
        """
        self.password = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """
        Verify a raw password against the stored hash.

        Parameters
        ----------
        raw_password : str
            The plain-text password to verify.

        Returns
        -------
        bool
            True if the password matches; otherwise False.
        """
        return check_password(raw_password, self.password)

    def __str__(self) -> str:
        """
        Return a string representation of the bank account.

        Returns
        -------
        str
            A string showing the account number and owner.
        """
        return f"Account {self.account_number} for {self.user}"


class Payment(models.Model):
    """
    Represents a payment made by a user for an order.

    Attributes
    ----------
    user : User
        The user who made the payment.
    order : Order
        The order associated with the payment.
    payment_date : datetime
        The date and time when the payment was created.
    amount : Decimal
        The amount paid for the order.
    method : str
        The payment method chosen by the user.
    status : str
        The status of the payment (Pending, Completed, Failed, Refunded).
    transaction_id : str or None
        Optional unique identifier for the payment transaction.
    """

    PAYMENT_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed"),
        ("Refunded", "Refunded"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("Credit Card", "Credit Card"),
        ("Debit Card", "Debit Card"),
        ("PayPal", "PayPal"),
        ("Bank Transfer", "Bank Transfer"),
        ("Cash on Delivery", "Cash on Delivery"),
        ("bKash", "bKash"),
        ("Rocket", "Rocket"),
        ("Apple Pay", "Apple Pay"),
        ("Google Pay", "Google Pay"),
        ("Master Card", "Master Card"),
        ("Nagad", "Nagad"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment",
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        default="Credit Card",
    )
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="Pending",
    )
    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
    )

    def __str__(self) -> str:
        """
        Return a string representation of the payment.

        Returns
        -------
        str
            A string showing the payment ID, associated order ID, and status.
        """
        return f"Payment {self.id} for Order {self.order.id} - Status: {self.status}"