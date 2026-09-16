from django.db import models


class DiscountCode(models.Model):
    """
    Represents a discount code that can be applied to purchases.
    
    Attributes:
        code (str): A unique identifier for the discount code.
        description (str): A brief description of the discount.
        discount_percentage (Decimal): The percentage discount provided by the code.
        valid_from (datetime): The start date and time of the discount's validity.
        valid_to (datetime): The end date and time of the discount's validity.
        is_active (bool): Indicates whether the discount code is currently active.
    """

    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
