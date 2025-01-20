from django.test import TestCase
from api.models import Kebab

class FiltersTestCase(TestCase):
    def setUp(self):
        # Reset bazy przed każdym testem
        Kebab.objects.all().delete()

        # Tworzenie danych testowych
        self.kebab_open1 = Kebab.objects.create(
            name="Open Kebab 1",
            latitude=51.1,
            longitude=16.2,
            status="open"
        )
        self.kebab_open2 = Kebab.objects.create(
            name="Open Kebab 2",
            latitude=51.3,  # Poza zakresem latitude dla test_filter_by_combined_criteria
            longitude=16.25,
            status="open"
        )
        self.kebab_closed = Kebab.objects.create(
            name="Closed Kebab",
            latitude=51.5,
            longitude=16.5,
            status="closed"
        )
        self.kebab_legnica = Kebab.objects.create(
            name="Legnica Kebab",
            latitude=51.2,
            longitude=16.15,
            status="open"
        )

    def test_filter_by_status(self):
        # Filtrowanie kebabów o statusie 'open'
        open_kebabs = Kebab.objects.filter(status="open")
        self.assertEqual(open_kebabs.count(), 3)
        self.assertIn(self.kebab_open1, open_kebabs)
        self.assertIn(self.kebab_legnica, open_kebabs)

    def test_filter_by_latitude_longitude(self):
        # Filtrowanie kebabów w okolicach Legnicy
        legnica_kebabs = Kebab.objects.filter(
            latitude__gte=51.15, latitude__lte=51.25,
            longitude__gte=16.1, longitude__lte=16.2
        )
        self.assertEqual(legnica_kebabs.count(), 1)
        self.assertEqual(legnica_kebabs.first().name, "Legnica Kebab")

    def test_no_results_for_invalid_filter(self):
        # Brak wyników dla niewłaściwych współrzędnych
        out_of_range_kebabs = Kebab.objects.filter(latitude__lt=50, longitude__gt=17)
        self.assertEqual(out_of_range_kebabs.count(), 0)

    def test_filter_with_invalid_status(self):
        # Brak wyników dla statusu, który nie istnieje
        invalid_status_kebabs = Kebab.objects.filter(status="nonexistent")
        self.assertEqual(invalid_status_kebabs.count(), 0)

    def test_filter_by_partial_name(self):
        # Filtrowanie po częściowej nazwie
        partial_name_kebabs = Kebab.objects.filter(name__icontains="Open")
        self.assertEqual(partial_name_kebabs.count(), 2)
        self.assertIn(self.kebab_open1, partial_name_kebabs)

    def test_filter_excluding_status(self):
        # Wykluczanie kebabów o statusie 'closed'
        non_closed_kebabs = Kebab.objects.exclude(status="closed")
        self.assertEqual(non_closed_kebabs.count(), 3)
        self.assertNotIn(self.kebab_closed, non_closed_kebabs)

    def test_filter_by_combined_criteria(self):
        # Filtrowanie po statusie 'open' i zakresie latitude
        filtered_kebabs = Kebab.objects.filter(
            status="open", latitude__gte=51.1, latitude__lte=51.25
        )
        self.assertEqual(filtered_kebabs.count(), 2)
        self.assertIn(self.kebab_open1, filtered_kebabs)
        self.assertIn(self.kebab_legnica, filtered_kebabs)
