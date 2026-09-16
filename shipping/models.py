from django.db import models

# Create your models here.

class ShippingMethod(models.Model):
    """
    Represents a shipping method offered to customers.

    Attributes:
        method (str): The type of shipping method, chosen from predefined options.
        charge (Decimal): The cost of using this shipping method.
        estimated_delivery_time (str): A description of the estimated delivery time.
        is_active (bool): Indicates whether this shipping method is currently available.
    """

    METHOD_CHOICES = [
        ('standard', 'Standard Shipping'),
        ('express', 'Express Shipping'),
        ('overnight', 'Overnight Shipping'),
        ('two_day', 'Two-Day Shipping'),
        ('same_day', 'Same-Day Shipping'),
        ('international', 'International Shipping'),
    ]

    method = models.CharField(max_length=20, choices=METHOD_CHOICES, unique=True)
    charge = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_delivery_time = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_method_display()} - ${self.charge}"
