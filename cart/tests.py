from django.test import TestCase
from products.models import Product
from users.models import UserProfile
from cart.models import Cart, CartItem


class CartModelTestCase(TestCase):
    """
    Test suite for the Cart and CartItem models.
    """

    def setUp(self):
        """
        Set up test data for the Cart and CartItem models.

        Creates:
            - A test user.
            - Two test products with all required fields.
            - A cart associated with the test user.
        """
        # Create a test user
        self.user = UserProfile.objects.create(
            username='testuser',
            email='testuser@example.com',
        )
        # Create test products
        self.product1 = Product.objects.create(
            name='Test Product 1',
            brand='Brand A',
            product_type='Electronics',
            size='Medium',
            color='Black',
            year_of_manufacture=2022,
            price=100.0,
            rating=4.5,
        )
        self.product2 = Product.objects.create(
            name='Test Product 2',
            brand='Brand B',
            product_type='Clothing',
            size='Large',
            color='Red',
            year_of_manufacture=2023,
            price=200.0,
            rating=4.0,
        )
        # Create a cart for the user
        self.cart = Cart.objects.create(user=self.user)

    def test_add_cart_item(self):
        """
        Test adding a CartItem to the Cart.

        Verifies:
            - The CartItem's total price is calculated correctly.
            - The item count in the cart increases.
        """
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product1,
            quantity=2
        )
        self.assertEqual(cart_item.total_price, 200.0)
        self.assertEqual(self.cart.items.count(), 1)

    def test_cart_total_price(self):
        """
        Test calculating the total price of the Cart.

        Adds multiple CartItems to the cart and verifies:
            - The total price of the cart is calculated accurately.
        """
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)  # 2 * 100 = 200
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)  # 1 * 200 = 200
        self.assertEqual(self.cart.total, 400.0)

    def test_remove_cart_item(self):
        """
        Test removing an item from the Cart.

        Verifies:
            - The item count decreases after removal.
        """
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        self.assertEqual(self.cart.items.count(), 1)
        cart_item.delete()
        self.assertEqual(self.cart.items.count(), 0)

    def test_update_cart_item_quantity(self):
        """
        Test updating the quantity of a CartItem.

        Verifies:
            - The CartItem's quantity is updated correctly.
            - The total price of the CartItem is recalculated accurately.
        """
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=1)
        cart_item.quantity = 3
        cart_item.save()
        self.assertEqual(cart_item.quantity, 3)
        self.assertEqual(cart_item.total_price, 300.0)

    def test_empty_cart(self):
        """
        Test emptying the cart.

        Verifies:
            - The total price of the cart is zero after emptying.
            - The item count in the cart is zero after emptying.
        """
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=1)
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)
        self.cart.items.all().delete()
        self.assertEqual(self.cart.total, 0)
        self.assertEqual(self.cart.items.count(), 0)

    def test_string_representation(self):
        """
        Test the string representations of Cart and CartItem.

        Verifies:
            - The Cart string includes the associated user's information.
            - The CartItem string includes the quantity and product name.
        """
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        self.assertEqual(str(self.cart), f"Cart for {self.user}")
        self.assertEqual(str(cart_item), "2 x Test Product 1")
