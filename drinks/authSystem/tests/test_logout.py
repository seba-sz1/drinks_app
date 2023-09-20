from django.contrib.auth.models import User
from django.test.testcases import TestCase
from django.urls import reverse


class TestLogout(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123')

    def test_logout(self):
        self.client.login(username='testuser', password='123')
        response = self.client.get(reverse('logout_user'))
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

    def test_logout_view_when_user_not_login(self):
        self.client.logout()
        response = self.client.get((reverse('logout_user')))
        self.assertRedirects(response, '/login/?next=/logout/', status_code=302, target_status_code=200)
