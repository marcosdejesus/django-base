from django.test import TestCase
from django.urls import reverse
from django.core import mail

from django.contrib.auth.models import User

class PasswordResetMailTests(TestCase):
    def setUp(self):
        User.objects.create_user('testin', 'testin@test.com','1senhadotestin')
        self.response = self.client.post(reverse('users:password_reset'),
                                         {'email': 'testin@test.com'})
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual(self.email.subject,'[Uptime Notifier] Please reset your password')

    def test_email_to(self):
        self.assertSequenceEqual(self.email.to, ['testin@test.com',])

    def test_email_body(self):
        uidb64 = self.response.context.get('uid')
        token = self.response.context.get('token')

        self.assertIn(reverse('users:password_reset_confirm',
                              kwargs={'uidb64':uidb64,'token': token}),
                      self.email.body)
        self.assertIn('testin', self.email.body)
        self.assertIn('testin@test.com', self.email.body)
