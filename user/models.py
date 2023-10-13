from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True, unique=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True, default='profiles/default-profile-pic.png')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username