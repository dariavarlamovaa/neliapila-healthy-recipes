from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea
from .models import Profile, Contact


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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Profile.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is already in use')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 15:
            raise forms.ValidationError('Username cannot contain more than 15 characters')

        if Profile.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This username is already in use')

        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].widget = forms.FileInput(attrs={'accept': 'image/*'})


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'subject', 'body']

        labels = {'body': ''}

    def __init__(self, *args, **kwargs):
        authenticated = kwargs.pop('authenticated', False)
        super().__init__(*args, **kwargs)

        self.fields['body'].widget = Textarea(attrs={'placeholder': 'Write your message here'})
        if authenticated:
            del self.fields['email']
        else:
            self.fields['email'].required = True