from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True,
                             label='Email address')

    class Meta():
        model = User
        fields = ("username", "email")
