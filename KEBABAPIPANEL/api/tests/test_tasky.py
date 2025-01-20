from django.test import TestCase
from unittest.mock import patch, MagicMock
from api.models import Kebab
from api.tasky import update_kebab_details

class TaskTestCase(TestCase):
    def setUp(self):
        # Tworzenie danych testowych
        self.kebab = Kebab.objects.create(
            name="Test Kebab",
            latitude=51.1,
            longitude=16.2,
            status="open",
            pyszne_url="https://www.pyszne.pl/test-kebab"
        )

    @patch("api.fetchers.GoogleRatingsFetcher.fetch_google_rating")
    @patch("api.fetchers.PyszneRatingsFetcher.fetch_pyszne_details")
    def test_update_kebab_details_success(self, mock_pyszne_fetch, mock_google_fetch):
        # Mockowanie zwracanych danych z GoogleRatingsFetcher
        mock_google_fetch.return_value = {
            "rating": 4.5,
            "place_id": "123456",
            "logo_url": "http://example.com/logo.png"
        }
        # Mockowanie zwracanych danych z PyszneRatingsFetcher
        mock_pyszne_fetch.return_value = {
            "rating": 4.2,
            "logo_url": "http://pyszne.com/logo.png"
        }

        # Wywołanie funkcji aktualizującej
        update_kebab_details()

        # Sprawdzenie wyników
        self.kebab.refresh_from_db()
        self.assertEqual(self.kebab.google_rating, 4.5)
        self.assertEqual(self.kebab.pyszne_rating, 4.2)
        self.assertEqual(self.kebab.logo.name, "http://example.com/logo.png")

    @patch("api.fetchers.GoogleRatingsFetcher.fetch_google_rating")
    @patch("api.fetchers.PyszneRatingsFetcher.fetch_pyszne_details")
    def test_update_kebab_details_no_data(self, mock_pyszne_fetch, mock_google_fetch):
        # Mockowanie zwracania pustych danych
        mock_google_fetch.return_value = None
        mock_pyszne_fetch.return_value = None

        # Wywołanie funkcji aktualizującej
        update_kebab_details()

        # Sprawdzenie wyników
        self.kebab.refresh_from_db()
        self.assertIsNone(self.kebab.google_rating)
        self.assertIsNone(self.kebab.pyszne_rating)
        self.assertEqual(self.kebab.logo.name, '')

    @patch("api.fetchers.GoogleRatingsFetcher.fetch_google_rating")
    @patch("api.fetchers.PyszneRatingsFetcher.fetch_pyszne_details")
    def test_update_kebab_details_exception_handling(self, mock_pyszne_fetch, mock_google_fetch):
        # Mockowanie wyjątku w GoogleRatingsFetcher
        mock_google_fetch.side_effect = Exception("Google API Error")
        # Mockowanie wyjątku w PyszneRatingsFetcher
        mock_pyszne_fetch.side_effect = Exception("Pyszne API Error")

        # Wywołanie funkcji aktualizującej
        update_kebab_details()

        # Sprawdzenie, że dane nie zostały zmienione
        self.kebab.refresh_from_db()
        self.assertIsNone(self.kebab.google_rating)
        self.assertIsNone(self.kebab.pyszne_rating)
        self.assertEqual(self.kebab.logo.name, '')
