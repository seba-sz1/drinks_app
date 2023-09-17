from django.contrib.auth.models import User
from django.test import Client
from django.test.testcases import TestCase


class TestLogout(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='123')

    def test_logout(self):
        self.client.login(username='testuser', password='123')
        response = self.client.get('/logout/', follow=True)
        self.assertRedirects(response, '/', target_status_code=200)
