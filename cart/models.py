'''from django.db import models
from products.models import Product
from users.models import UserProfile


class Cart(models.Model):
    """
    Represents a shopping cart associated with a specific user.

    Attributes:
        user (UserProfile): The user who owns the cart.
        created_at (DateTimeField): The date and time when the cart was created.
        updated_at (DateTimeField): The date and time when the cart was last updated.
    """
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='carts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return a string representation of the cart.
        """
        return f"Cart for {self.user}"

    @property
    def total(self):
        """
        Calculate the total price of all items in the cart.

        Returns:
            float: The total price of all cart items.
        """
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    """
    Represents an individual item in a shopping cart.

    Attributes:
        cart (Cart): The cart to which this item belongs.
        product (Product): The product associated with this item.
        quantity (PositiveIntegerField): The quantity of the product in the cart.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        """
        Return a string representation of the cart item.
        """
        return f"{self.quantity} x {self.product}"

    @property
    def total_price(self):
        """
        Calculate the total price for this cart item.

        Returns:
            float: The total price (product price multiplied by quantity).
        """
        return self.product.price * self.quantity
'''



# # cart/models.py
# from django.db import models
# from products.models import Product
# from users.models import UserProfile

# class Cart(models.Model):
#     user = models.ForeignKey(
#         UserProfile,
#         on_delete=models.CASCADE,
#         related_name='carts'
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Cart for {self.user}"

#     @property
#     def total(self):
#         return sum(item.total_price for item in self.items.all())

# class CartItem(models.Model):
#     cart = models.ForeignKey(
#         Cart,
#         on_delete=models.CASCADE,
#         related_name='items'
#     )
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"{self.quantity} x {self.product}"

#     @property
#     def total_price(self):
#         return self.product.price * self.quantity

# cart/models.py
from django.db import models
from products.models import Product
from users.models import UserProfile

class Cart(models.Model):
    """
    A shopping cart model that stores items selected by a user.

    Attributes
    ----------
    user : UserProfile
        The user who owns the cart.
    created_at : datetime
        The timestamp when the cart was created.
    updated_at : datetime
        The timestamp when the cart was last updated.
    items : QuerySet of CartItem
        Related items belonging to this cart.
    """

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='carts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return a string representation of the cart.

        Returns
        -------
        str
            A string showing the cart owner.
        """
        return f"Cart for {self.user}"

    @property
    def total(self):
        """
        Calculate the total price of all items in the cart.

        Returns
        -------
        float
            The total price of all items in the cart.
        """
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    """
    A model representing an item inside a shopping cart.

    Attributes
    ----------
    cart : Cart
        The cart to which this item belongs.
    product : Product
        The product added to the cart.
    quantity : int
        The number of units of the product.
    """

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        """
        Return a string representation of the cart item.

        Returns
        -------
        str
            A string showing the quantity and product name.
        """
        return f"{self.quantity} x {self.product}"

    @property
    def total_price(self):
        """
        Calculate the total price for this cart item.

        Returns
        -------
        float
            The total price (product price multiplied by quantity).
        """
        return self.product.price * self.quantity