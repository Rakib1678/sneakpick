from django.test import TestCase
from django.urls import reverse
from .models import Product


class ProductSearchViewTest(TestCase):
    """
    Test suite for the product search view.

    These tests verify:
    - Searching by different fields (name, brand, product_type)
    - Sorting results by price, rating, and name
    - Handling empty queries and no-result scenarios
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create sample product data used across all search tests.
        """
        Product.objects.create(
            name="Red Sneakers",
            brand="BrandA",
            product_type="GradeA",
            size="10",
            color="Red",
            year_of_manufacture=2022,
            price=100.00,
            rating=4.5,
        )
        Product.objects.create(
            name="Blue Sneakers",
            brand="BrandB",
            product_type="GradeB",
            size="9",
            color="Blue",
            year_of_manufacture=2023,
            price=120.00,
            rating=4.7,
        )
        Product.objects.create(
            name="Green Sneakers",
            brand="BrandC",
            product_type="GradeB",
            size="11",
            color="Green",
            year_of_manufacture=2021,
            price=80.00,
            rating=4.2,
        )

    def test_search_by_name(self):
        """
        Test searching by exact product name.

        Expected
        --------
        - 'Red Sneakers' should appear
        - Other products should not appear
        """
        response = self.client.get(reverse('products:search'), {'q': 'Red Sneakers'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Red Sneakers")
        self.assertNotContains(response, "Blue Sneakers")
        self.assertNotContains(response, "Green Sneakers")

    def test_search_by_brand(self):
        """
        Test searching by brand name.

        Expected
        --------
        Only 'Blue Sneakers' should match BrandB.
        """
        response = self.client.get(reverse('products:search'), {'q': 'BrandB'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blue Sneakers")
        self.assertNotContains(response, "Red Sneakers")
        self.assertNotContains(response, "Green Sneakers")

    def test_search_by_product_type(self):
        """
        Test searching by product_type field.

        Expected
        --------
        Only GradeA product should appear.
        """
        response = self.client.get(reverse('products:search'), {'q': 'GradeA'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Red Sneakers")
        self.assertNotContains(response, "Blue Sneakers")
        self.assertNotContains(response, "Green Sneakers")

    def test_sort_by_price_asc(self):
        """
        Test sorting results by price in ascending order.

        Expected order
        --------------
        1. 80.00
        2. 100.00
        3. 120.00
        """
        response = self.client.get(reverse('products:search'),
                                   {'q': 'Sneakers', 'sort_by': 'price', 'sort_order': 'asc'})
        results = list(response.context['results'])
        self.assertEqual(results[0].price, 80.00)
        self.assertEqual(results[1].price, 100.00)
        self.assertEqual(results[2].price, 120.00)

    def test_sort_by_rating_desc(self):
        """
        Test sorting results by rating in descending order.

        Expected order
        --------------
        4.7 → 4.5 → 4.2
        """
        response = self.client.get(reverse('products:search'),
                                   {'q': 'Sneakers', 'sort_by': 'rating', 'sort_order': 'desc'})
        results = list(response.context['results'])
        self.assertEqual(results[0].rating, 4.7)
        self.assertEqual(results[1].rating, 4.5)
        self.assertEqual(results[2].rating, 4.2)

 

    def test_empty_query(self):
        """
        Test behavior when no search query is provided.

        Expected
        --------
        The page should show a message asking for a query.
        """
        response = self.client.get(reverse('products:search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a search query.")

    def test_no_results(self):
        """
        Test behavior when no products match the search query.

        Expected
        --------
        A 'no results' message should be displayed.
        """
        response = self.client.get(reverse('products:search'), {'q': 'Yellow Sneakers'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No products found. Please refine your search.")



class ProductListViewTest(TestCase):
    """
    Test suite for the product list (filter) view.

    These tests verify:
    - Filtering by individual fields
    - Combined filtering
    - Case-insensitive matching
    - Handling invalid fields
    - Handling empty filters
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create sample product data used across all filter tests.
        """
        Product.objects.create(
            name="Red Sneakers",
            brand="BrandA",
            product_type="GradeA",
            size="10",
            color="Red",
            year_of_manufacture=2022,
            price=100.00,
            rating=4.5,
        )
        Product.objects.create(
            name="Blue Sneakers",
            brand="BrandB",
            product_type="GradeB",
            size="9",
            color="Blue",
            year_of_manufacture=2023,
            price=120.00,
            rating=4.7,
        )
        Product.objects.create(
            name="Green Sneakers",
            brand="BrandC",
            product_type="GradeB",
            size="11",
            color="Green",
            year_of_manufacture=2021,
            price=80.00,
            rating=4.2,
        )

    def test_filter_by_name(self):
        """
        Test filtering by exact product name.
        """
        response = self.client.get(reverse('products:product_list'), {'name': 'Blue Sneakers'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().name, "Red Sneakers")

    def test_filter_by_brand(self):
        """
        Test filtering by brand field.
        """
        response = self.client.get(reverse('products:product_list'), {'brand': 'BrandA'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().brand, "BrandB")

    def test_filter_by_price(self):
        """
        Test filtering by exact price.
        """
        response = self.client.get(reverse('products:product_list'), {'price': '100.00'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().price, 100.00)

    def test_filter_by_year_of_manufacture(self):
        """
        Test filtering by manufacturing year.
        """
        response = self.client.get(reverse('products:product_list'), {'year_of_manufacture': '2023'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().year_of_manufacture, 2023)

    def test_filter_by_combined_fields(self):
        """
        Test filtering using multiple fields at once.

        Expected
        --------
        Only Blue Sneakers should match BrandB + Blue.
        """
        response = self.client.get(reverse('products:product_list'),
                                   {'brand': 'BrandB', 'color': 'Blue'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().name, "Blue Sneakers")

    def test_empty_query(self):
        """
        Test behavior when no filters are applied.

        Expected
        --------
        All products should be returned.
        """
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 3)

    def test_no_results(self):
        """
        Test behavior when filters match no products.
        """
        response = self.client.get(reverse('products:product_list'), {'name': 'Yellow Sneakers'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 0)

    def test_invalid_field(self):
        """
        Test behavior when an invalid filter field is provided.

        Expected
        --------
        Invalid fields should be ignored and all products returned.
        """
        response = self.client.get(reverse('products:product_list'), {'invalid_field': 'test'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 3)

    def test_filter_by_rating(self):
        """
        Test filtering by exact rating value.
        """
        response = self.client.get(reverse('products:product_list'), {'rating': '4.7'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().rating, 4.7)

    def test_case_insensitive_filter(self):
        """
        Test case-insensitive filtering for text fields.
        """
        response = self.client.get(reverse('products:product_list'), {'name': 'red sneakers'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().name, "Red Sneakers")


class ProductAdvancedFilterTests(TestCase):
    """
    Test suite for advanced filtering logic such as price ranges.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create sample products for advanced filtering tests.
        """
        Product.objects.create(
            name="Budget Sneakers",
            brand="BrandX",
            product_type="GradeC",
            size="8",
            color="Black",
            year_of_manufacture=2024,
            price=50.00,
            rating=4.0,
        )
        Product.objects.create(
            name="Premium Sneakers",
            brand="BrandX",
            product_type="GradeC",
            size="9",
            color="White",
            year_of_manufacture=2024,
            price=200.00,
            rating=4.9,
        )
        Product.objects.create(
            name="Midrange Sneakers",
            brand="BrandY",
            product_type="GradeB",
            size="10",
            color="Blue",
            year_of_manufacture=2023,
            price=120.00,
            rating=4.5,
        )

    def test_filter_by_brand_and_price_range(self):
        """
        Test filtering by brand combined with a price range.

        Expected
        --------
        Only 'Budget Sneakers' should match BrandX + price between 40 and 100.
        """
        response = self.client.get(reverse('products:product_list'), {
            'brand': 'BrandX',
            'min_price': '40',
            'max_price': '100',
        })
        products = response.context['products']
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().name, "Budget Sneakers")