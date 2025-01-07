from django.test import TestCase, Client
from api.models import Kebab, Suggestion
from django.contrib.auth.models import User
from django.urls import reverse
import json

class KebabModelTestCase(TestCase):
    def setUp(self):
        self.kebab = Kebab.objects.create(
            name="Test Kebab",
            description="A delicious kebab.",
            latitude=50.0,
            longitude=19.0,
            rating=4.5,
            opening_hours="9 AM - 10 PM",
            status="open"
        )

    def test_kebab_creation(self):
        self.assertEqual(self.kebab.name, "Test Kebab")

    def test_kebab_update(self):
        self.kebab.name = "Updated Kebab"
        self.kebab.save()
        self.assertEqual(self.kebab.name, "Updated Kebab")

    def test_kebab_rating_update(self):
        self.kebab.rating = 5.0
        self.kebab.save()
        self.assertEqual(self.kebab.rating, 5.0)

    def test_kebab_social_links(self):
        self.kebab.social_links = {"facebook": "http://facebook.com/testkebab"}
        self.kebab.save()
        self.assertEqual(self.kebab.social_links["facebook"], "http://facebook.com/testkebab")

    def test_kebab_default_status(self):
        kebab = Kebab.objects.create(
            name="Default Status Kebab",
            description="A kebab with default status.",
            latitude=50.0,
            longitude=19.0
        )
        self.assertEqual(kebab.status, "open")


class SuggestionModelTestCase(TestCase):
    def setUp(self):
        self.suggestion = Suggestion.objects.create(
            title="New Location Suggestion",
            description="Open a new kebab shop in Warsaw."
        )

    def test_suggestion_creation(self):
        self.assertEqual(self.suggestion.title, "New Location Suggestion")

    def test_suggestion_status_update(self):
        self.suggestion.status = "Accepted"
        self.suggestion.save()
        self.assertEqual(self.suggestion.status, "Accepted")

    def test_suggestion_default_status(self):
        self.assertEqual(self.suggestion.status, "Pending")


class UserTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="adminpass"
        )
        self.client = Client()

    def test_admin_creation(self):
        self.assertTrue(self.admin_user.is_superuser)
        self.assertTrue(self.admin_user.is_staff)

    def test_password_change(self):
        self.admin_user.set_password("newpassword")
        self.admin_user.save()
        self.assertTrue(self.admin_user.check_password("newpassword"))

    def test_admin_login(self):
        response = self.client.post(reverse("login"), {
            "username": "admin",
            "password": "adminpass"
        })
        self.assertEqual(response.status_code, 200)


class KebabViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.kebab = Kebab.objects.create(
            name="View Test Kebab",
            description="A viewable kebab.",
            latitude=50.0,
            longitude=19.0,
            rating=4.5,
            opening_hours="9 AM - 10 PM",
            status="open"
        )

    def test_kebab_list_view(self):
        response = self.client.get(reverse("kebab_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Test Kebab")

    def test_kebab_detail_view(self):
        response = self.client.get(reverse("kebab_detail", args=[self.kebab.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A viewable kebab.")

    def test_kebab_edit_view(self):
        response = self.client.post(reverse("kebab_edit", args=[self.kebab.id]), {
            "name": "Edited Kebab",
            "description": "An updated kebab.",
            "opening_hours": "10 AM - 9 PM",
            "status": "closed"
        })
        self.assertEqual(response.status_code, 302)  # Redirect after edit
        self.kebab.refresh_from_db()
        self.assertEqual(self.kebab.name, "Edited Kebab")

    def test_social_links_edit_view(self):
        response = self.client.post(reverse("kebab_edit_social_links", args=[self.kebab.id]), {
            "social_links": json.dumps({"facebook": "http://facebook.com/newkebab"})
        })
        self.assertEqual(response.status_code, 302)  # Redirect after edit
        self.kebab.refresh_from_db()
        self.assertEqual(self.kebab.social_links["facebook"], "http://facebook.com/newkebab")


class SuggestionViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.suggestion = Suggestion.objects.create(
            title="Suggestion for Testing",
            description="Test description for suggestion."
        )

    def test_suggestion_list_view(self):
        response = self.client.get(reverse("suggestion_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Suggestion for Testing")

    def test_suggestion_accept_view(self):
        response = self.client.post(reverse("suggestion_accept", args=[self.suggestion.id]))
        self.assertEqual(response.status_code, 302)
        self.suggestion.refresh_from_db()
        self.assertEqual(self.suggestion.status, "Accepted")

    def test_suggestion_reject_view(self):
        response = self.client.post(reverse("suggestion_reject", args=[self.suggestion.id]))
        self.assertEqual(response.status_code, 302)
        self.suggestion.refresh_from_db()
        self.assertEqual(self.suggestion.status, "Rejected")


class AdditionalTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_fetch_kebab_api_structure(self):
        Kebab.objects.create(name="API Test Kebab", latitude=50.0, longitude=19.0)
        response = self.client.get("/api/kebabs/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            '[{"id":1,"name":"API Test Kebab","latitude":50.0,"longitude":19.0}]'
        )

    def test_invalid_kebab_id(self):
        response = self.client.get("/api/kebabs/999/")
        self.assertEqual(response.status_code, 404)

    def test_create_kebab_without_required_fields(self):
        response = self.client.post(reverse("kebab_edit"), {})
        self.assertEqual(response.status_code, 400)  # Validation error

    def test_login_required_for_edit(self):
        response = self.client.post(reverse("kebab_edit", args=[1]), {"name": "Restricted"})
        self.assertEqual(response.status_code, 302)  # Redirect to login
