from django import forms
from django.forms import ModelForm

from .models import Recipe


class NewRecipe(ModelForm):
    class Meta:
        model = Recipe
        exclude = ['author', 'is_approved', 'date_created']
        labels = {'image': 'Recipe image',
                  'ingredients': 'Ingredients and Their Quantity'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].widget = forms.FileInput(attrs={'accept': 'image/*'})
        self.fields['ingredients'].widget = forms.Textarea(
            attrs={'placeholder': 'Ingredient1 - 100g\nIngredient2 - 2 spoons'})
        self.fields['steps'].widget = forms.Textarea(
            attrs={'placeholder': 'Step 1 - ...\nStep 2 - ...'})
