from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Kebab, UserComment, Favorite, OpeningHour

class ModelsTestCase(TestCase):
    def setUp(self):
        # Tworzenie danych testowych
        self.user = User.objects.create_user(username="testuser", password="password")
        self.kebab = Kebab.objects.create(
            name="Test Kebab",
            description="Delicious kebab",
            latitude=51.1,
            longitude=16.2,
            status="open",
            opening_year=2000,
            closing_year=2020
        )
        self.opening_hour = OpeningHour.objects.create(
            kebab=self.kebab,
            hours={
                "monday": {"open": "09:00", "close": "21:00"},
                "tuesday": {"open": "09:00", "close": "21:00"}
            }
        )

    def test_create_kebab(self):
        # Sprawdza, czy obiekt Kebab został poprawnie utworzony
        self.assertEqual(str(self.kebab), "Test Kebab")
        self.assertEqual(self.kebab.status, "open")

    def test_kebab_latitude_validation(self):
        # Walidacja błędnych współrzędnych latitude
        kebab = Kebab(name="Invalid Kebab", latitude=100.0, longitude=16.2)
        with self.assertRaises(Exception):
            kebab.full_clean()  # Wymuszenie walidacji

    def test_kebab_longitude_validation(self):
        # Walidacja błędnych współrzędnych longitude
        kebab = Kebab(name="Invalid Kebab", latitude=51.1, longitude=200.0)
        with self.assertRaises(Exception):
            kebab.full_clean()  # Wymuszenie walidacji


    def test_kebab_opening_closing_year(self):
        # Sprawdza poprawność lat otwarcia i zamknięcia
        self.kebab.closing_year = 1990
        with self.assertRaises(Exception):
            self.kebab.full_clean()

    def test_create_user_comment(self):
        # Tworzenie komentarza użytkownika
        comment = UserComment.objects.create(user=self.user, kebab=self.kebab, text="Great!")
        self.assertEqual(str(comment), "testuser - Test Kebab")
        self.assertEqual(comment.text, "Great!")

    def test_create_favorite(self):
        # Tworzenie ulubionego kebaba
        favorite = Favorite.objects.create(user=self.user, kebab=self.kebab)
        self.assertEqual(str(favorite), "testuser - Test Kebab")
        self.assertEqual(favorite.user, self.user)
        self.assertEqual(favorite.kebab, self.kebab)

    def test_opening_hours(self):
        # Sprawdza poprawność modelu OpeningHour
        self.assertEqual(str(self.opening_hour), "Test Kebab - {'monday': {'open': '09:00', 'close': '21:00'}, 'tuesday': {'open': '09:00', 'close': '21:00'}}")
        self.assertIn("monday", self.opening_hour.hours)

    def test_unique_favorite_constraint(self):
        # Sprawdza ograniczenie unikalności w modelu Favorite
        Favorite.objects.create(user=self.user, kebab=self.kebab)
        with self.assertRaises(Exception):
            Favorite.objects.create(user=self.user, kebab=self.kebab)
