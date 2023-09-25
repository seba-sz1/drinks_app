from django.contrib.auth.models import User
from django.test import Client
from django.test.testcases import TestCase
from django.urls import reverse


class TestRegister(TestCase):

    def setUp(self):
        self.existing_username = 'existinguser'
        self.new_username = 'testuser'
        self.existing_email = 'testuser@wp.pl'
        self.new_email = 'newuser@wp.pl'
        self.password = 'test123456'
        self.new_password = 'newabc123456'
        self.too_simple_password = 'abc'
        self.test_form = {
            'username': self.new_username,
            'email': self.new_email,
            'password1': self.new_password,
            'password2': self.new_password
        }
        self.existing_user = User.objects.create_user(self.existing_username, self.existing_email, self.password)

    def test_get_register_form(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_when_user_correctly_created(self):
        response = self.client.post(reverse('register'), data=self.test_form)

        self.assertEqual(response.status_code, 302)
        users = User.objects.all()
        self.assertEqual(users.count(), 2)

    def test_register_when_username_already_exists(self):
        self.test_form['username'] = self.existing_username

        response = self.client.post(reverse('register'), data=self.test_form)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        users = User.objects.all()
        self.assertEqual(users.count(), 1)

    def test_register_when_email_already_exists(self):
        self.test_form['email'] = self.existing_email

        response = self.client.post(reverse('register'), data=self.test_form)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        users = User.objects.all()
        self.assertEqual(users.count(), 1)

    def test_register_when_passwords_not_match(self):
        self.test_form['password1'] = self.password
        self.test_form['password2'] = self.new_password

        response = self.client.post(reverse('register'), data=self.test_form)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        users = User.objects.all()
        self.assertEqual(users.count(), 1)

    def test_register_when_new_password_too_simple(self):
        self.test_form['password1'] = self.too_simple_password
        self.test_form['password2'] = self.too_simple_password

        response = self.client.post(reverse('register'), data=self.test_form)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_method_not_allowed(self):
        methods = [
            Client.delete,
            Client.put,
            Client.patch,
        ]

        for method in methods:
            with self.subTest(method=method):
                response = method(self.client, (reverse('register')))
                self.assertEqual(response.status_code, 405)
