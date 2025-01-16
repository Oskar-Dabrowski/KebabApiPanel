from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from api.models import Kebab, OpeningHour, Suggestion


class KebabModelTest(TestCase):
    def setUp(self):
        self.kebab = Kebab.objects.create(
            name="Testowy Kebab",
            description="Delicious kebab description.",
            latitude=51.2095,
            longitude=16.1554,
            contact="123-456-789",
            meats="Chicken, Lamb",
            sauces="Garlic, Spicy",
            status="open",
            social_links={"facebook": "http://facebook.com/testkebab"},
            google_rating=4.5,
            pyszne_rating=4.2
        )

    def test_kebab_creation(self):
        """Test creating a Kebab object."""
        self.assertEqual(self.kebab.name, "Testowy Kebab")
        self.assertEqual(self.kebab.status, "open")

    def test_kebab_str_method(self):
        """Test the __str__ method of the Kebab model."""
        self.assertEqual(str(self.kebab), "Testowy Kebab")

    def test_kebab_geolocation(self):
        """Test the geolocation attributes of a Kebab."""
        self.assertEqual(self.kebab.latitude, 51.2095)
        self.assertEqual(self.kebab.longitude, 16.1554)

    def test_kebab_optional_fields(self):
        """Test optional fields like description, meats, sauces, and social_links."""
        self.assertEqual(self.kebab.description, "Delicious kebab description.")
        self.assertEqual(self.kebab.contact, "123-456-789")
        self.assertEqual(self.kebab.meats, "Chicken, Lamb")
        self.assertEqual(self.kebab.sauces, "Garlic, Spicy")
        self.assertEqual(self.kebab.social_links, {"facebook": "http://facebook.com/testkebab"})
        self.assertEqual(self.kebab.google_rating, 4.5)
        self.assertEqual(self.kebab.pyszne_rating, 4.2)


class SuggestionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.kebab = Kebab.objects.create(
            name="Testowy Kebab",
            latitude=51.2095,
            longitude=16.1554
        )
        self.suggestion = Suggestion.objects.create(
            user=self.user,
            kebab=self.kebab,
            title="Propozycja",
            description="Opis propozycji"
        )

    def test_suggestion_creation(self):
        """Test creating a Suggestion object."""
        self.assertEqual(self.suggestion.status, "Pending")

    def test_mark_as_accepted(self):
        """Test marking a suggestion as accepted."""
        self.suggestion.mark_as_accepted()
        self.assertEqual(self.suggestion.status, "Accepted")

    def test_mark_as_rejected(self):
        """Test marking a suggestion as rejected."""
        self.suggestion.mark_as_rejected()
        self.assertEqual(self.suggestion.status, "Rejected")

    def test_suggestion_str_method(self):
        """Test the __str__ method of the Suggestion model."""
        self.assertEqual(str(self.suggestion), "Propozycja - Testowy Kebab")


class OpeningHourModelTest(TestCase):
    def setUp(self):
        self.kebab = Kebab.objects.create(
            name="Testowy Kebab",
            latitude=51.2095,
            longitude=16.1554
        )
        self.opening_hour = OpeningHour.objects.create(
            kebab=self.kebab,
            hours={
                "monday": {"open": "10:00", "close": "22:00"},
                "tuesday": {"open": "10:00", "close": "22:00"},
                "wednesday": {"open": "10:00", "close": "22:00"},
                "thursday": {"open": "10:00", "close": "22:00"},
                "friday": {"open": "10:00", "close": "22:00"},
                "saturday": {"open": "10:00", "close": "22:00"},
                "sunday": {"open": "10:00", "close": "22:00"}
            }
        )

    def test_opening_hour_creation(self):
        """Test creating an OpeningHour object."""
        self.assertEqual(self.opening_hour.hours["monday"]["open"], "10:00")
        self.assertEqual(self.opening_hour.hours["monday"]["close"], "22:00")

    def test_opening_hour_str_method(self):
        """Test the __str__ method of the OpeningHour model."""
        expected_start = "Testowy Kebab - {'monday': {'open': '10:00', 'close': '22:00'}, 'tuesday': {'open': '10:00', 'close': '22:00'}, ..."
        self.assertTrue(str(self.opening_hour).startswith(expected_start))
    def test_opening_hour_validation(self):
        """Test the clean() method for validating hours JSON structure."""
        invalid_hours = {
            "monday": {"open": "10:00"},  # Missing 'close'
            "tuesday": {},  # Missing 'open' and 'close'
            "wednesday": "invalid",  # Invalid type
        }
        self.opening_hour.hours = invalid_hours
        with self.assertRaises(ValidationError):
            self.opening_hour.clean()

