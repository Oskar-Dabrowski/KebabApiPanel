from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import Kebab, UserComment, Favorite

class APITestCase(TestCase):
    def setUp(self):
        Kebab.objects.all().delete()  # Usuwanie wszystkich kebabów przed każdym testem
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.kebab = Kebab.objects.create(
            name="Test Kebab",
            description="Delicious kebab",
            latitude=51.1234,
            longitude=16.1234,
            status="open"
        )

    def test_register_user(self):
        # Test endpoint for registering a new user
        response = self.client.post('/api/register_user', {'email': 'newuser@test.com', 'password': 'password123'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('message'), "User registered successfully")

    def test_login_user(self):
        # Test endpoint for logging in an existing user
        response = self.client.post('/api/login_user', {'email': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())

    def test_kebab_list(self):
        response = self.client.get('/api/kebabs')
        self.assertEqual(response.status_code, 200)
        # Weryfikuj obiekt po nazwie
        kebab_names = [kebab['name'] for kebab in response.json()]
        self.assertIn("Test Kebab", kebab_names)



    def test_kebab_detail(self):
        # Test endpoint for retrieving details of a specific kebab
        response = self.client.get(f'/api/kebabs/{self.kebab.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], "Test Kebab")

    def test_add_favorite(self):
        # Test endpoint for adding a kebab to user's favorites
        response = self.client.post(f'/api/kebabs/{self.kebab.id}/favorite')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Favorite.objects.filter(user=self.user, kebab=self.kebab).exists())

    def test_add_user_comment(self):
        # Test endpoint for adding a comment to a kebab
        response = self.client.post(f'/api/kebabs/{self.kebab.id}/comment', {'text': 'Great kebab!'})
        self.assertEqual(response.status_code, 201)
        comments = UserComment.objects.filter(kebab=self.kebab)
        self.assertEqual(comments.count(), 1)
        self.assertEqual(comments.first().text, 'Great kebab!')
