# KEBABAPIPANEL/api/tests/test_filters.py

from django.test import TestCase
from api.models import Kebab

class KebabFilterTest(TestCase):
    def setUp(self):
        # Create test kebabs
        Kebab.objects.create(name="Kebab 1", status="open", latitude=51.2095, longitude=16.1554)
        Kebab.objects.create(name="Kebab 2", status="closed", latitude=52.2095, longitude=17.1554)

    def test_filter_by_status(self):
        # Filter kebabs by status
        open_kebabs = Kebab.objects.filter(status="open")

        # Assert that only the open kebab is returned
        self.assertEqual(open_kebabs.count(), 1)
        self.assertEqual(open_kebabs.first().name, "Kebab 1")

    def test_filter_by_name(self):
        # Filter kebabs by name
        kebab_2 = Kebab.objects.filter(name="Kebab 2")

        # Assert that the correct kebab is returned
        self.assertEqual(kebab_2.count(), 1)
        self.assertEqual(kebab_2.first().status, "closed")

    def test_combined_filters(self):
        # Filter kebabs by name and status
        kebab = Kebab.objects.filter(name="Kebab 1", status="open")

        # Assert that the correct kebab is returned
        self.assertEqual(kebab.count(), 1)
        self.assertEqual(kebab.first().latitude, 51.2095)

    def test_no_matching_filters(self):
        # Attempt to filter kebabs with a non-matching status
        no_kebabs = Kebab.objects.filter(status="nonexistent")

        # Assert that no kebabs are returned
        self.assertEqual(no_kebabs.count(), 0)
