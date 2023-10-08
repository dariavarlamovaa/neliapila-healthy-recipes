from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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

