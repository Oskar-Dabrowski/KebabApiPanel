from django.test import TestCase
from unittest.mock import patch
from api.tasky import update_kebab_details
from api.models import Kebab

class CeleryTaskTest(TestCase):
    @patch("api.fetchers.GoogleRatingsFetcher.fetch_google_rating")
    @patch("api.fetchers.PyszneRatingsFetcher.fetch_pyszne_rating")
    def test_update_kebab_details(self, mock_pyszne, mock_google):
        # Mocking fetch_google_rating and fetch_pyszne_rating methods
        mock_google.return_value = {"rating": 4.5}
        mock_pyszne.return_value = {"rating": 4.0}

        # Create a test Kebab object
        kebab = Kebab.objects.create(
            name="Test Kebab",
            latitude=51.2095,
            longitude=16.1554,
            status="open"
        )

        # Call the task to be tested
        result = update_kebab_details()
        self.assertIsNone(result)

        # Ensure the mocked methods were called
        mock_google.assert_called_once_with(kebab.name)
        mock_pyszne.assert_called_once_with(kebab.name)

    def test_update_kebab_details_no_data(self):
        # Mocking fetch_google_rating to return None (no data)
        with patch("api.fetchers.GoogleRatingsFetcher.fetch_google_rating", return_value=None):
            # Create a test Kebab object
            Kebab.objects.create(
                name="Test Kebab",
                latitude=51.2095,
                longitude=16.1554,
                status="open"
            )

            # Call the task to be tested
            result = update_kebab_details()
            self.assertIsNone(result)
