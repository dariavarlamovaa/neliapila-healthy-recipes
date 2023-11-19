from django.contrib.auth.models import User
from django.db import models

from recipes.models import Recipe


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=500, blank=True, null=True, unique=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True, default='profiles/default-profile-pic.png')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Favorite(models.Model):
    favorite_recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.favorite_recipe.title


class Contact(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.subject}'