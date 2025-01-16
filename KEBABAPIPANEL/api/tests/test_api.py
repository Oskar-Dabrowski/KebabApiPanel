from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Kebab
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class KebabAPITest(APITestCase):
    def setUp(self):
        # Create a test user and authenticate
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Create test data
        self.kebab1 = Kebab.objects.create(name="Kebab 1", latitude=51.1, longitude=16.2, status="open")
        self.kebab2 = Kebab.objects.create(name="Kebab 2", latitude=51.2, longitude=16.3, status="closed")
        self.kebab_list_url = '/api/kebabs'
        self.kebab_detail_url = f'/api/kebabs/{self.kebab1.id}'

    def test_get_kebab_list(self):
        response = self.client.get(self.kebab_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_post_kebab(self):
        # Adjusted for correct serializer fields
        data = {
            "title": "Kebab 3",  # Matches 'title' in serializer
            "location": "New location",  # Matches 'description' in serializer
            "latitude": 51.3,
            "longitude": 16.4,
            "status": "open"  # Ensure this matches model constraints
        }
        response = self.client.post(self.kebab_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], "Kebab 3")  # Check 'title' in response

    def test_invalid_post_kebab(self):
        # Ensure invalid data matches serializer validation constraints
        data = {
            "title": "",  # Empty title
            "latitude": None,  # Missing latitude
            "longitude": None,  # Missing longitude
            "status": ""  # Empty status
        }
        response = self.client.post(self.kebab_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_kebab(self):
        # Update fields; ensure consistency with serializer
        data = {
            "title": "Updated Kebab",  # Matches 'title' in serializer
            "status": "closed"
        }
        response = self.client.patch(self.kebab_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], "Updated Kebab")  # Check 'title' in response

    def test_delete_kebab(self):
        # Delete a kebab and check for proper cleanup
        response = self.client.delete(self.kebab_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(self.kebab_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
