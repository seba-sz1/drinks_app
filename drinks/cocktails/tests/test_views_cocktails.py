from django.test.testcases import TestCase
from django.test import Client
from django.urls import reverse


class TestCocktails(TestCase):

    def test_home_view_correctly_display_when_not_login(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view_correctly_display_when_login(self):
        self.client.login(username='testuser', password='test123456')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
