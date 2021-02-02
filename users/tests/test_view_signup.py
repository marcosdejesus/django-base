from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from ..views import signup
from ..forms import SignUpForm

# Create your tests here.
class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('users:signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_signup_return_right_view(self):
        view = resolve('/users/signup/')
        self.assertEqual(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        '''
        The view must contain five inputs: csrf, username, email, password1,
        and password2
        '''
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)

class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('users:signup')
        data = {
            'username': 'testin',
            'email': 'testin@test.com',
            'password1': '1senhadotestin',
            'password2': '1senhadotestin'
        }

        self.response = self.client.post(url, data)
        self.home_url = '/'

    def test_signup_redirection(self):
        '''
        A valid form submission should redirect to the application home page
        '''
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        '''
        A valid form submission should create a user in the Database
        '''
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        '''
        Create a new request to an arbitrary page
        The response should have a `user` in its context after a successful
        login.
        '''
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class InvalidSignUpTests(TestCase):
    def setUp(self):
        self.response = self.client.post(reverse('users:signup'))

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_user_not_created(self):
        self.assertFalse(User.objects.exists())
