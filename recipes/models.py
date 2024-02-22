import os
from django.utils import timezone
from django.db import models


def recipe_image_path(instance, filename):
    author_name = instance.author.username
    post_date = timezone.now().date()
    return os.path.join('recipes_images', str(post_date), author_name, filename)


class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snacks', 'Snacks'),
        ('Desserts', 'Desserts'),
        ('Drinks', 'Drinks'),
        ('Miscellaneous', 'Other')
    ]
    STATUS_CHOICES = [
        (True, 'Approved'),
        (False, 'On moderation'),
    ]
    author = models.ForeignKey('user.Profile', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50)
    portions = models.PositiveIntegerField(default=1, blank=True, null=True)
    cooking_hours = models.PositiveIntegerField(default=0)
    cooking_minutes = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to=recipe_image_path)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    ingredients = models.TextField()
    steps = models.TextField()
    is_approved = models.BooleanField(default=False, choices=STATUS_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    RATING_CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    STATUS_CHOICES = [
        (True, 'Approved'),
        (False, 'On moderation'),
    ]
    owner = models.ForeignKey('user.Profile', on_delete=models.SET_NULL, null=True, blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    body = models.TextField(max_length=500, null=True, blank=True)
    rating = models.IntegerField(null=False, blank=False, choices=RATING_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False, choices=STATUS_CHOICES)

    def __str__(self):
        return f'Rating: {self.rating}. Recipe: {self.recipe}'

    class Meta:
        unique_together = [['owner', 'recipe'], ]
