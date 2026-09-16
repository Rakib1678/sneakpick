from django.db import models


class Product(models.Model):
    """
    Represents a product in the catalog.

    This model stores all essential product information including:
    - Basic attributes (name, brand, product_type)
    - Physical attributes (size, color)
    - Manufacturing details (year_of_manufacture)
    - Commercial attributes (price, rating)
    - Media (image)

    Fields
    ------
    name : CharField
        The name of the product.
    brand : CharField
        The brand or manufacturer of the product.
    product_type : CharField
        The category or type of the product.
    size : CharField
        The size specification of the product.
    color : CharField
        The color of the product.
    year_of_manufacture : PositiveIntegerField
        The year the product was manufactured.
    price : DecimalField
        The price of the product with two decimal precision.
    rating : FloatField
        The average rating of the product (default = 0).
    image : ImageField
        The product image stored in the 'products/' directory.

    Notes
    -----
    - The rating field is updated using the `update_rating` method.
    - The image field defaults to 'default.png' if no image is uploaded.
    """

    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    product_type = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    year_of_manufacture = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(default=0)
    image = models.ImageField(upload_to='products/', default='default.png', blank=True)

    def __str__(self):
        """
        Return the string representation of the product.

        Returns
        -------
        str
            The product's name.
        """
        return self.name

    def update_rating(self):
        """
        Update the product's average rating based on associated reviews.

        This method fetches all reviews linked to the product, calculates
        the average rating, and updates the product's `rating` field.

        Notes
        -----
        - Uses a lazy import of Reviews to avoid circular import issues.
        - Saves the updated rating to the database only if reviews exist.
        """
        from users.models import Reviews  # Lazy import to avoid circular import error

        reviews = Reviews.objects.filter(product=self)
        if reviews.exists():
            total_rating = sum(review.rating for review in reviews)
            self.rating = total_rating / len(reviews)
            self.save()