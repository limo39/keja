from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from base.models import Property
from datetime import date, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample property data for testing'

    def handle(self, *args, **options):
        # Create sample users (landlords)
        sample_users = [
            {'username': 'landlord1', 'email': 'landlord1@example.com', 'name': 'John Smith'},
            {'username': 'landlord2', 'email': 'landlord2@example.com', 'name': 'Sarah Johnson'},
            {'username': 'landlord3', 'email': 'landlord3@example.com', 'name': 'Mike Wilson'},
        ]

        users = []
        for user_data in sample_users:
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'username': user_data['username'],
                    'name': user_data['name'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {user.email}')
            users.append(user)

        # Sample property data
        sample_properties = [
            {
                'title': 'Modern Downtown Apartment',
                'property_type': 'apartment',
                'rent_amount': 1200.00,
                'location': 'Downtown',
                'address': '123 Main Street, Downtown District',
                'bedrooms': 2,
                'bathrooms': 2,
                'area_sqft': 850,
                'description': 'Beautiful modern apartment in the heart of downtown. Walking distance to restaurants, shops, and public transportation.',
                'amenities': 'WiFi, Parking, Gym, Pool, Laundry',
            },
            {
                'title': 'Cozy Studio Near University',
                'property_type': 'studio',
                'rent_amount': 800.00,
                'location': 'University District',
                'address': '456 College Ave, University District',
                'bedrooms': 1,
                'bathrooms': 1,
                'area_sqft': 450,
                'description': 'Perfect for students! Cozy studio apartment just 5 minutes walk from the university campus.',
                'amenities': 'WiFi, Parking, Study Area',
            },
            {
                'title': 'Spacious Family House',
                'property_type': 'house',
                'rent_amount': 2500.00,
                'location': 'Suburbs',
                'address': '789 Oak Street, Suburban Heights',
                'bedrooms': 4,
                'bathrooms': 3,
                'area_sqft': 2200,
                'description': 'Large family home with backyard, perfect for families with children. Quiet neighborhood with great schools nearby.',
                'amenities': 'WiFi, Parking, Garden, Garage, Pet Friendly',
            },
            {
                'title': 'Luxury Condo with City View',
                'property_type': 'condo',
                'rent_amount': 1800.00,
                'location': 'Midtown',
                'address': '321 Skyline Blvd, Midtown',
                'bedrooms': 3,
                'bathrooms': 2,
                'area_sqft': 1200,
                'description': 'Stunning luxury condo with panoramic city views. High-end finishes and modern amenities.',
                'amenities': 'WiFi, Parking, Gym, Pool, Concierge, City View',
            },
            {
                'title': 'Charming Townhouse',
                'property_type': 'townhouse',
                'rent_amount': 1600.00,
                'location': 'Historic District',
                'address': '654 Heritage Lane, Historic District',
                'bedrooms': 3,
                'bathrooms': 2,
                'area_sqft': 1400,
                'description': 'Beautiful townhouse in historic district with original hardwood floors and modern updates.',
                'amenities': 'WiFi, Parking, Fireplace, Patio',
            },
            {
                'title': 'Budget-Friendly Apartment',
                'property_type': 'apartment',
                'rent_amount': 900.00,
                'location': 'East Side',
                'address': '987 Budget St, East Side',
                'bedrooms': 1,
                'bathrooms': 1,
                'area_sqft': 600,
                'description': 'Affordable apartment perfect for young professionals. Clean, safe, and well-maintained.',
                'amenities': 'WiFi, Parking, Laundry',
            },
        ]

        # Create properties
        for i, prop_data in enumerate(sample_properties):
            landlord = users[i % len(users)]  # Rotate through users
            
            property_obj, created = Property.objects.get_or_create(
                title=prop_data['title'],
                landlord=landlord,
                defaults={
                    **prop_data,
                    'date_available': date.today() + timedelta(days=random.randint(1, 30)),
                    'is_available': True,
                }
            )
            
            if created:
                self.stdout.write(f'Created property: {property_obj.title}')
            else:
                self.stdout.write(f'Property already exists: {property_obj.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data! '
                f'Users: {len(users)}, Properties: {Property.objects.count()}'
            )
        )