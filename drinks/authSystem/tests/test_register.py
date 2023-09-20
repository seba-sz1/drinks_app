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
        self.valid_form = {
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
        response = self.client.post(reverse('register'), data=self.valid_form)

        self.assertEqual(response.status_code, 302)
        users = User.objects.all()
        self.assertEqual(users.count(), 2)

    def test_register_when_username_already_exists(self):
        existing_username_form = dict(self.valid_form)
        existing_username_form['username'] = self.existing_username

        response = self.client.post(reverse('register'), data=existing_username_form)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        users = User.objects.all()
        self.assertEqual(users.count(), 1)

    def test_register_when_email_already_exists(self):
        existing_email_form = dict(self.valid_form)
        existing_email_form['email'] = self.existing_email

        response = self.client.post(reverse('register'), data=existing_email_form)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        users = User.objects.all()
        self.assertEqual(users.count(), 1)

    def test_register_when_passwords_not_match(self):
        password_not_match_form = dict(self.valid_form)
        password_not_match_form['password1'] = self.password
        password_not_match_form['password2'] = self.new_password

        response = self.client.post(reverse('register'), data=password_not_match_form)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        users = User.objects.all()
        self.assertEqual(users.count(), 1)

    def test_register_when_new_password_too_simple(self):
        password_too_simple_form = dict(self.valid_form)
        password_too_simple_form['password1'] = self.too_simple_password
        password_too_simple_form['password2'] = self.too_simple_password

        response = self.client.post(reverse('register'), data=password_too_simple_form)

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
