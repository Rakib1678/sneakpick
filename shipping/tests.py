from django.test import TestCase
from decimal import Decimal
from .models import ShippingMethod
from .views import shipping_Methods


class ShippingMethodModelTest(TestCase):
    """
    Test cases for the ShippingMethod model.
    """

    def setUp(self):
        """
        Set up test data for the ShippingMethod model.
        """
        self.shipping_method1 = ShippingMethod.objects.create(
            method="standard",
            charge=Decimal('5.00'),
            estimated_delivery_time="5-7 Business Days",
            is_active=True,
        )
        self.shipping_method2 = ShippingMethod.objects.create(
            method="express",
            charge=Decimal('15.00'),
            estimated_delivery_time="1-2 Business Days",
            is_active=True,
        )
        self.shipping_method3 = ShippingMethod.objects.create(
            method="overnight",
            charge=Decimal('30.00'),
            estimated_delivery_time="Next Day",
            is_active=False,
        )

    def test_shipping_method_creation(self):
        """
        Test that shipping methods are created correctly.
        """
        self.assertEqual(self.shipping_method1.method, "standard")
        self.assertEqual(self.shipping_method1.charge, Decimal('5.00'))
        self.assertEqual(
            self.shipping_method1.estimated_delivery_time, "5-7 Business Days"
        )
        self.assertTrue(self.shipping_method1.is_active)

    def test_shipping_method_unique(self):
        """
        Ensure the 'method' field is unique.
        """
        with self.assertRaises(Exception):
            ShippingMethod.objects.create(
                method="standard",  # Duplicate method
                charge=Decimal('6.00'),
                estimated_delivery_time="3-5 Business Days",
                is_active=True,
            )

    def test_active_shipping_methods(self):
        """
        Test that only active shipping methods are returned.
        """
        active_shipping_methods = ShippingMethod.objects.filter(is_active=True)
        self.assertEqual(active_shipping_methods.count(), 2)  # Two active methods
        self.assertIn(self.shipping_method1, active_shipping_methods)
        self.assertIn(self.shipping_method2, active_shipping_methods)

    def test_inactive_shipping_methods(self):
        """
        Test that inactive shipping methods are excluded.
        """
        inactive_shipping_methods = ShippingMethod.objects.filter(is_active=False)
        self.assertEqual(inactive_shipping_methods.count(), 1)  # One inactive method
        self.assertIn(self.shipping_method3, inactive_shipping_methods)

    def test_shipping_method_charge(self):
        """
        Test that the charge is stored correctly and is a decimal type.
        """
        self.assertEqual(self.shipping_method1.charge, Decimal('5.00'))
        self.assertGreater(self.shipping_method2.charge, self.shipping_method1.charge)
        self.assertEqual(self.shipping_method3.charge, Decimal('30.00'))

    def test_shipping_method_string_representation(self):
        """
        Test the string representation of a shipping method.
        """
        self.assertEqual(str(self.shipping_method1), "Standard Shipping - $5.00")
        self.assertEqual(str(self.shipping_method2), "Express Shipping - $15.00")

    def test_shipping_method_estimated_delivery_time(self):
        """
        Test that the estimated delivery time is stored and retrieved correctly.
        """
        self.assertEqual(
            self.shipping_method1.estimated_delivery_time, "5-7 Business Days"
        )
        self.assertEqual(
            self.shipping_method2.estimated_delivery_time, "1-2 Business Days"
        )
        self.assertEqual(self.shipping_method3.estimated_delivery_time, "Next Day")

    def test_active_shipping_method_count(self):
        """
        Test the number of active shipping methods.
        """
        active_shipping_method_count = ShippingMethod.objects.filter(
            is_active=True
        ).count()
        self.assertEqual(active_shipping_method_count, 2)

    def test_shipping_method_choices(self):
        """
        Test that the method choices are correct.
        """
        self.assertEqual(self.shipping_method1.method, "standard")
        self.assertEqual(self.shipping_method2.method, "express")
        self.assertEqual(self.shipping_method3.method, "overnight")
