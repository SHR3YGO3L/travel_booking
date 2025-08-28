from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import TravelOption, Booking
from datetime import datetime

class TravelBookingTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()

        # Create some travel options
        self.option1 = TravelOption.objects.create(
            type='Flight',
            source='Mumbai',
            destination='Delhi',
            datetime=datetime(2025, 9, 1, 9, 0),
            price=3500,
            available_seats=100
        )
        self.option2 = TravelOption.objects.create(
            type='Train',
            source='Chennai',
            destination='Bangalore',
            datetime=datetime(2025, 9, 5, 14, 30),
            price=500,
            available_seats=150
        )

    def test_travel_options_list(self):
        # Test travel options page loads and shows existing options
        response = self.client.get(reverse('travel_options'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mumbai')
        self.assertContains(response, 'Chennai')

    def test_register_user(self):
        # Test registration with valid data
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        })
        self.assertRedirects(response, reverse('travel_options'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_logout(self):
        # Login
        login = self.client.login(username='testuser', password='testpass')
        self.assertTrue(login)

        # Logout
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_book_travel_success(self):
        self.client.login(username='testuser', password='testpass')
        
        response = self.client.post(reverse('book_travel', args=[self.option1.id]), {
            'number_of_seats': 2,
        })
        self.assertRedirects(response, reverse('my_bookings'))
        booking = Booking.objects.get(user=self.user, travel_option=self.option1)
        self.assertEqual(booking.number_of_seats, 2)
        self.option1.refresh_from_db()
        self.assertEqual(self.option1.available_seats, 98)  # seats reduced

    def test_book_travel_insufficient_seats(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('book_travel', args=[self.option1.id]), {
            'number_of_seats': 200,
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'number_of_seats', 'Not enough available seats.')

    def test_my_bookings_view_requires_login(self):
        # Should redirect to login if not logged in
        response = self.client.get(reverse('my_bookings'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('my_bookings')}")

    def test_cancel_booking(self):
        self.client.login(username='testuser', password='testpass')
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.option2,
            number_of_seats=1,
            total_price=500,
            status='Confirmed'
        )
        response = self.client.get(reverse('cancel_booking', args=[booking.id]))
        self.assertRedirects(response, reverse('my_bookings'))
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'Cancelled')
        self.option2.refresh_from_db()
        self.assertEqual(self.option2.available_seats, 151)  # seat returned

