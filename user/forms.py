from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Password confirmation'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

