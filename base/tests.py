from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, timedelta
from .models import Property, Topic

User = get_user_model()


class PropertyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_property_creation(self):
        """Test that a property can be created successfully"""
        property_obj = Property.objects.create(
            landlord=self.user,
            title='Test Property',
            property_type='apartment',
            rent_amount=Decimal('1200.00'),
            location='Test City',
            address='123 Test Street',
            bedrooms=2,
            bathrooms=1,
            area_sqft=800,
            description='A nice test property',
            date_available=date.today() + timedelta(days=30)
        )
        
        self.assertEqual(property_obj.title, 'Test Property')
        self.assertEqual(property_obj.landlord, self.user)
        self.assertEqual(property_obj.rent_amount, Decimal('1200.00'))
        self.assertTrue(property_obj.is_available)

    def test_property_str_method(self):
        """Test the string representation of Property model"""
        property_obj = Property.objects.create(
            landlord=self.user,
            title='Test Property',
            property_type='apartment',
            rent_amount=Decimal('1200.00'),
            location='Test City',
            address='123 Test Street',
            bedrooms=2,
            bathrooms=1,
            area_sqft=800,
            description='A nice test property',
            date_available=date.today() + timedelta(days=30)
        )
        
        expected_str = f"Test Property - $1200.00/month"
        self.assertEqual(str(property_obj), expected_str)


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a test property
        self.property = Property.objects.create(
            landlord=self.user,
            title='Test Property',
            property_type='apartment',
            rent_amount=Decimal('1200.00'),
            location='Test City',
            address='123 Test Street',
            bedrooms=2,
            bathrooms=1,
            area_sqft=800,
            description='A nice test property',
            date_available=date.today() + timedelta(days=30)
        )

    def test_home_page_loads(self):
        """Test that the home page loads successfully"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Find Your Perfect Rental')

    def test_home_page_shows_properties(self):
        """Test that properties are displayed on the home page"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Property')

    def test_property_search_by_location(self):
        """Test searching properties by location"""
        response = self.client.get(reverse('home'), {'location': 'Test City'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Property')

    def test_property_search_by_price_range(self):
        """Test searching properties by price range"""
        response = self.client.get(reverse('home'), {
            'min_price': '1000',
            'max_price': '1500'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Property')


class PropertyDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.property = Property.objects.create(
            landlord=self.user,
            title='Test Property',
            property_type='apartment',
            rent_amount=Decimal('1200.00'),
            location='Test City',
            address='123 Test Street',
            bedrooms=2,
            bathrooms=1,
            area_sqft=800,
            description='A nice test property',
            date_available=date.today() + timedelta(days=30)
        )

    def test_property_detail_page_loads(self):
        """Test that property detail page loads successfully"""
        response = self.client.get(reverse('property_detail', args=[self.property.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Property')
        self.assertContains(response, '$1200.00/month')


class UserAuthenticationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_registration(self):
        """Test user registration functionality"""
        response = self.client.post(reverse('register'), {
            'name': 'Test User',
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        })
        
        # Should redirect after successful registration
        self.assertEqual(response.status_code, 302)
        
        # Check if user was created
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_user_login(self):
        """Test user login functionality"""
        # Create a user first
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        
        # Should redirect after successful login
        self.assertEqual(response.status_code, 302)


class PropertyFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = Client()
        self.client.force_login(self.user)

    def test_add_property_page_requires_login(self):
        """Test that add property page requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('add_property'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_add_property_page_loads_for_authenticated_user(self):
        """Test that authenticated users can access add property page"""
        response = self.client.get(reverse('add_property'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add New Property')