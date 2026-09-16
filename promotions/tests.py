from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from .models import DiscountCode


class DiscountCodeModelTest(TestCase):
    """
    Test suite for validating the DiscountCode model.

    This class contains unit tests that verify:
    - String representation of the model
    - Correct storage of decimal discount values
    - Validity period logic (valid_from and valid_to)
    - Active/inactive status behavior
    - Discount calculation logic
    """

    def setUp(self):
        """
        Set up a reusable DiscountCode instance for all tests.

        Creates a sample discount code:
        - Code: WINTER25
        - Discount: 25%
        - Valid for 7 days from now
        - Active status: True
        """
        self.discount = DiscountCode.objects.create(
            code="WINTER25",
            description="25% off winter collection",
            discount_percentage=Decimal("25.00"),
            valid_from=timezone.now(),
            valid_to=timezone.now() + timezone.timedelta(days=7),
            is_active=True
        )

    def test_str_method_returns_code(self):
        """
        Test the __str__ method of DiscountCode.

        Ensures that converting the model instance to a string
        returns the discount code itself.

        Expected
        -------
        "WINTER25"
        """
        self.assertEqual(str(self.discount), "WINTER25")

    def test_discount_percentage_field(self):
        """
        Test that the discount_percentage field stores the correct decimal value.

        Verifies that the model preserves the exact Decimal value assigned.

        Expected
        -------
        Decimal("25.00")
        """
        self.assertEqual(self.discount.discount_percentage, Decimal("25.00"))

    def test_validity_period(self):
        """
        Test that the discount is valid within its date range.

        Checks that the current time falls between valid_from and valid_to.
        """
        now = timezone.now()
        self.assertTrue(self.discount.valid_from <= now <= self.discount.valid_to)

    def test_is_active_flag(self):
        """
        Test the is_active flag behavior.

        Ensures that the discount is considered active when is_active=True.
        """
        self.assertTrue(self.discount.is_active)

    def test_expired_discount(self):
        """
        Test that expired discounts are not considered valid.

        Creates a discount code whose validity period ended 5 days ago
        and verifies that the current time does not fall within its range.
        """
        expired = DiscountCode.objects.create(
            code="OLD10",
            description="10% off old stock",
            discount_percentage=Decimal("10.00"),
            valid_from=timezone.now() - timezone.timedelta(days=10),
            valid_to=timezone.now() - timezone.timedelta(days=5),
            is_active=True
        )
        now = timezone.now()
        self.assertFalse(expired.valid_from <= now <= expired.valid_to)

    def test_apply_discount_helper(self):
        """
        Test the discount calculation logic.

        Applies a 25% discount to an amount of 200.00 and verifies
        that the final price is calculated correctly.

        Calculation
        -----------
        25% of 200 = 50  
        Final price = 200 - 50 = 150

        Expected
        -------
        Decimal("150.00")
        """
        amount = Decimal("200.00")
        discount_value = (self.discount.discount_percentage / Decimal(100)) * amount
        final_price = amount - discount_value
        self.assertEqual(final_price, Decimal("150.00"))