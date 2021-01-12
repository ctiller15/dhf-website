from django.test import TestCase, Client
from django.contrib import auth
from django.contrib.auth.models import AnonymousUser, User
from users.forms import CustomUserCreationForm

class UserTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_dashboard(self):
        response = self.client.get('/dashboard/')

        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(user.is_authenticated)
        self.assertContains(response, 'Login', status_code=200)

    def test_dashboard_logged_in(self):
        test_user_name = 'test'
        test_password = '123abc'
        test_email = 'testemail@testemail.com'

        User.objects.create_user(test_user_name, email=test_email, password=test_password)
        self.client.login(username=test_user_name, password=test_password)

        response = self.client.get('/dashboard/')

        self.assertContains(response, test_user_name, status_code=200)
        self.assertContains(response, 'Logout', status_code=200)
        self.assertContains(response, 'Change password', status_code=200)
        self.assertNotContains(response, 'Login', status_code=200)

    def test_login_page(self):
        response = self.client.get('/accounts/login/')

        self.assertEqual(response.status_code, 200)

    def test_logout_button(self):
        test_user_name = 'test'
        test_password = '123abc'
        test_email = 'testemail@testemail.com'

        User.objects.create_user(test_user_name, email=test_email, password=test_password)
        self.client.login(username=test_user_name, password=test_password)

        user = auth.get_user(self.client)

        self.assertTrue(user.is_authenticated)
        response = self.client.get('/accounts/logout/')

        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.assertEqual(response.url, '/dashboard/')

    def test_password_change(self):
        test_user_name = 'test'
        test_password = '123abc'
        test_email = 'testemail@testemail.com'

        User.objects.create_user(test_user_name, email=test_email, password=test_password)
        self.client.login(username=test_user_name, password=test_password)

        response = self.client.get('/accounts/password_change/')

        self.assertEqual(response.status_code, 200)

    def test_password_reset(self):
        response = self.client.get('/accounts/password_reset/')
        self.assertEqual(response.status_code, 200)

    def test_user_creation_form(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@testuser.com',
            'password1': 'fahfkasfk4563453',
            'password2': 'fahfkasfk4563453',
        }

        form = CustomUserCreationForm(data)
        self.assertTrue(form.is_valid())
