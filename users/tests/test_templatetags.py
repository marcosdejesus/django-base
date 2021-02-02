from django.test import TestCase
from django import forms

from ..templatetags.form_tags import field_type, field_css_class

class SimpleForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class FieldTypeTests(TestCase):
    def test_field_widget_type(self):
        form = SimpleForm()
        self.assertEqual('TextInput', field_type(form['name']))
        self.assertEqual('PasswordInput', field_type(form['password']))

class FieldCSSClassTests(TestCase):
    def test_unbound_field(self):
        form = SimpleForm()
        self.assertEqual('form-control ', field_css_class(form['name']))

    def test_valid_form_field(self):
        form = SimpleForm({'name': 'Testin', 'password': 'Senha1234'})
        self.assertEqual('form-control is_valid',field_css_class(form['name']))
        self.assertEqual('form-control ',field_css_class(form['password']))

    def test_invalid_form_field(self):
        form = SimpleForm({'name': '', 'password': 'Senha1234'})
        self.assertEqual('form-control is_invalid',field_css_class(form['name']))
        self.assertEqual('form-control ',field_css_class(form['password']))
