from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile


class NewUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        labels = {
            'username': 'Username',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Password confirmation'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'created']
        labels = {'image': ''}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].widget = forms.FileInput(attrs={'accept': 'image/*'})
