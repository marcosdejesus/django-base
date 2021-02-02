from django.test import TestCase
from django.urls import reverse, resolve
from django.core import mail
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('users:password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/users/password_reset/')
        self.assertIs(view.func.view_class, auth_views.PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form,PasswordResetForm)

    def test_form_inputs(self):
        '''
        The response form must contain two inputs: csrf and email
        '''
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)

class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = 'testin@teste.com'
        User.objects.create_user('testin',email,'1senhadotestin')
        url = reverse('users:password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_redirection(self):
        '''
        A valid form submission should redirect the user to 'password_reset_done' view
        '''
        url = reverse('users:password_reset_done')
        self.assertRedirects(self.response, url)

    def test_send_email(self):
        '''
        A valid form submission should send one email
        '''
        self.assertEqual(len(mail.outbox),1)

class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('users:password_reset')
        self.response = self.client.post(url, {'email': 'notauseremail@test.com'})

    def test_redirection(self):
        '''
        Even email addresses that are not associated with an user should redirect
        to 'password_reset_done' view
        '''
        url = reverse('users:password_reset_done')
        self.assertRedirects(self.response, url)

    def test_no_email_sent(self):
        self.assertEqual(len(mail.outbox), 0)

class PasswordResetDoneTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('users:password_reset_done'))

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        self.assertIs(resolve('/users/password_reset/done/').func.view_class, auth_views.PasswordResetDoneView)

class PasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='Testin', email='testin@teste.com',
                                        password='1senhadotestin')
        #Create a valid reset link base on how django does it
        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)

        url = reverse('users:password_reset_confirm', kwargs={
            'uidb64': self.uid,
            'token': self.token})
        self.response = self.client.get(url, follow=True)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve(f'/users/reset/{self.uid}/{self.token}/')
        self.assertIs(view.func.view_class, auth_views.PasswordResetConfirmView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoke')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def test_form_inputs(self):
        '''
        The form must contain three inputs: two passwords and one csrf
        '''
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)
