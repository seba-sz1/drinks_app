from django.contrib.auth.models import User
from django.test import Client
from django.test.testcases import TestCase


class TestLogin(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='123')

    def test_get(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_user.html')

    def test_post(self):
        response = self.client.post("/login/", {'username': 'testuser', 'password': '123'})
        self.assertRedirects(response, '/dashboard/', status_code=302, target_status_code=200)

    def test_post_failed_password(self):
        response = self.client.post("/login/", {'username': 'testuser', 'password': 'abc'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_user.html')

    def test_post_failed_username(self):
        response = self.client.post("/login/", {'username': 'testuser2', 'password': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_user.html')

    def test_method_not_allowed(self):
        methods = [
            Client.delete,
            Client.put,
            Client.patch,
        ]

        for method in methods:
            response = method(self.client, "/login/")
            self.assertEqual(response.status_code, 405)
