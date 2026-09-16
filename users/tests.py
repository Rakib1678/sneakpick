from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import SignupForm
from .models import Wishlist
from products.models import Product
import json

class SignupViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('users:signup')

    def test_signup_view_post_valid_data(self):

        data = {
            'username': 'testuser',
            'password1': 'validpassword123',
            'password2': 'validpassword123',
            'email': 'testuser@example.com',
        }

        response = self.client.post(self.url, data)

        #ensure user is created and redirected to login
        user = get_user_model().objects.get(username='testuser')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(user.is_authenticated)

    def test_signup_view_post_password_mismatch(self):
        """Test signup with mismatched passwords."""
        data = {
            'username': 'testuser',
            'password1': 'validpassword123',
            'password2': 'invalidpassword123',
            'email': 'testuser@example.com',
        }

        response = self.client.post(self.url, data)

        # Ensure the response status code is 200 (form re-rendered with errors)
        self.assertEqual(response.status_code, 200)

        # Check if the specific error message is displayed in the response
        self.assertContains(response, "The two password fields didn’t match.")


    def test_signup_view_get(self):

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')
        self.assertIsInstance(response.context['form'], SignupForm)

User = get_user_model()

class UserViewTests(TestCase):
    """
    Test class for user-related views, including login, profile, and wishlist management.
    """

    def setUp(self):
        """
        Set up initial test data and environment.
        """
        # Initialize the Django test client
        self.client = Client()
        
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser', password='password', email='testuser@example.com'
        )
        
        # Create a sample product to be added to the wishlist
        self.product = Product.objects.create(
            name="Sample Product",
            brand="Sample Brand",
            product_type="Shoes",
            size="10",
            color="Black",
            year_of_manufacture=2023,
            price=100.00,
            rating=4.5
        )

    def test_login_view_success(self):
        """
        Test that a user can log in successfully and is redirected to the profile page.
        """
        # Define the login URL and the login credentials
        login_url = reverse('users:login')
        data = {'username': 'testuser', 'password': 'password'}
        
        # Make a POST request to the login view with valid credentials
        response = self.client.post(login_url, data)
        
        # Check that the response redirects to the profile page on successful login
        self.assertRedirects(response, reverse('users:profile'))

    def test_login_view_invalid_credentials(self):
        """
        Test that invalid login credentials do not authenticate the user.
        """
        # Define the login URL and the invalid login credentials
        login_url = reverse('users:login')
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        
        # Make a POST request with incorrect credentials
        response = self.client.post(login_url, data)
        
        # Check that the user is not redirected and receives a 200 OK response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password. Note that both fields may be case-sensitive.")

    def test_profile_view_authenticated(self):
        """
        Test that the profile page displays correctly for an authenticated user.
        """
        # Log in the test user
        self.client.login(username='testuser', password='password')
        
        # Access the profile page
        response = self.client.get(reverse('users:profile'))
        
        # Check that the page loads successfully with a 200 OK response
        self.assertEqual(response.status_code, 200)
        
        # Check that the response contains the username and wishlist
        self.assertContains(response, self.user.username)
        self.assertContains(response, "Wishlist")

    def test_add_to_wishlist(self):
        """
        Test adding a product to the user's wishlist.
        """
        # Log in the test user
        self.client.login(username='testuser', password='password')
        
        # Define the URL for adding to the wishlist
        url = reverse('users:add_to_wishlist')
        data = json.dumps({'product_id': self.product.id})
        
        # Make a POST request to add the product to the wishlist
        response = self.client.post(url, data, content_type="application/json")
        
        # Check the JSON response message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Product added to wishlist'})
        
        # Verify that the product was added to the wishlist
        self.assertTrue(Wishlist.objects.filter(user=self.user, product=self.product).exists())

    def test_remove_from_wishlist(self):
        """
        Test removing a product from the user's wishlist.
        """
        # First, add the product to the wishlist
        Wishlist.objects.create(user=self.user, product=self.product)
        
        # Log in the test user
        self.client.login(username='testuser', password='password')
        
        # Define the URL for removing from the wishlist
        url = reverse('users:remove_from_wishlist')
        data = json.dumps({'product_id': self.product.id})
        
        # Make a POST request to remove the product from the wishlist
        response = self.client.post(url, data, content_type="application/json")
        
        # Check the JSON response message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Product removed from wishlist'})
        
        # Verify that the product was removed from the wishlist
        self.assertFalse(Wishlist.objects.filter(user=self.user, product=self.product).exists())
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from products.models import Product
from users.models import Reviews
from django.http import HttpResponse

class ReviewCreationTest(TestCase):

    def setUp(self):
        # Create a test user and product
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(
            name="Test Product",
            brand="Test Brand",
            product_type="Test Type",
            size="Medium",
            color="Red",
            year_of_manufacture=2023,
            price=100.00
        )

    def test_create_review_valid(self):
        """Test that a user can create a valid review."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('users:create_review', args=[self.product.id]), {
            'review': 'Great product!',
            'rating': 5
        })
        # Check if the review was created and redirected to product detail page
        self.assertRedirects(response, reverse('products:product_detail', kwargs={'product_id': self.product.id}))
        self.assertEqual(Reviews.objects.count(), 1)
        review = Reviews.objects.first()
        self.assertEqual(review.review, 'Great product!')
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.user, self.user)

    def test_create_review_empty_review(self):
        """Test that an empty review text returns an error."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('users:create_review', args=[self.product.id]), {
            'review': '',
            'rating': 3
        })
        # Check if the error message is returned for empty review text
        self.assertEqual(response.status_code, 400)
        self.assertIn('Review and rating cannot be empty.', response.content.decode())

    def test_create_review_invalid_rating(self):
        """Test that an invalid rating returns an error."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('users:create_review', args=[self.product.id]), {
            'review': 'Good product',
            'rating': 6  # Invalid rating (out of range)
        })
        # Check if the error message is returned for invalid rating
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid rating value', response.content.decode())

    def test_create_review_not_logged_in(self):
        """Test that an unauthenticated user is redirected to login."""
        response = self.client.get(reverse('users:create_review', args=[self.product.id]))
        self.assertRedirects(response, f'{reverse("users:login")}?next={reverse("users:create_review", args=[self.product.id])}')
