from django.contrib.auth.models import User
from django.test import Client
from django.test.testcases import TestCase


class TestRegister(TestCase):

    def setUp(self):
        self.existing_user = User.objects.create_user('existinguser', 'test123@wp.pl', 'test123')
        self.client = Client()
        self.username = 'testuser'
        self.email = 'testuser@wp.pl'
        self.password = 'test123456'

    def test_get(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_post_user_created(self):
        response = self.client.post('/register/',
                                    {'username': self.username, 'email': self.email, 'password1': self.password,
                                     'password2': self.password})
        self.assertEqual(response.status_code, 302)
        users = User.objects.all()
        self.assertEqual(users.count(), 2)

    def test_post_user_already_exists(self):
        response = self.client.post('/register/',
                                    {'username': 'existinguser', 'email': 'test123@wp.pl', 'password1': 'test123',
                                     'password2': 'test123'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        users = User.objects.all()
        self.assertEqual(users.count(), 1)

    def test_method_not_allowed(self):
        methods = [
            Client.delete,
            Client.put,
            Client.patch,
        ]

        for method in methods:
            response = method(self.client, "/register/")
            self.assertEqual(response.status_code, 405)
