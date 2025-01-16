from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Kebab

class KebabListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create test data
        self.kebab1 = Kebab.objects.create(name="Kebab 1", status="open")
        self.kebab2 = Kebab.objects.create(name="Kebab 2", status="open")
        self.kebab3 = Kebab.objects.create(name="Kebab 3", status="closed")

    def test_get_kebab_list(self):
        url = reverse("kebab-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(len(response.json()), 3)

    def test_filter_kebab_by_status(self):
        url = reverse("kebab-list") + "?status=open"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(len(response.json()), 2)

    def test_sort_kebab_by_name(self):
        url = reverse("kebab-list") + "?ordering=name"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        kebab_names = [kebab["name"] for kebab in response.json()]
        self.assertEqual(kebab_names, ["Kebab 1", "Kebab 2", "Kebab 3"])


class KebabDetailViewTest(TestCase):
    def setUp(self):
        self.kebab = Kebab.objects.create(name="Kebab Szczegółowy", latitude=51.3, longitude=16.4)

    def test_kebab_detail_view(self):
        response = self.client.get(reverse('kebab_detail', args=[self.kebab.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kebab Szczegółowy")

    def test_kebab_detail_404(self):
        response = self.client.get(reverse('kebab_detail', args=[999]))
        self.assertEqual(response.status_code, 404)
