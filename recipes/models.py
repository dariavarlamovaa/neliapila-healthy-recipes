from django.contrib.auth.models import User
from django.db import models


class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snacks', 'Snacks'),
        ('Desserts', 'Desserts'),
        ('Drinks', 'Drinks'),
    ]
    STATUS_CHOICES = [
        (True, 'Approved'),
        (False, 'On moderation'),
    ]
    author = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    portions = models.PositiveIntegerField(default=1, blank=True, null=True)
    cooking_hours = models.PositiveIntegerField(default=0)
    cooking_minutes = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='recipe_images/%(title)s/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    ingredients = models.JSONField(default=dict)
    steps = models.TextField()
    is_approved = models.BooleanField(default=False, choices=STATUS_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)
