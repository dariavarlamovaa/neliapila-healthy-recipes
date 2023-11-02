from django.forms import ModelForm, FileInput, Textarea

from .models import Recipe, Comment


class NewRecipe(ModelForm):
    class Meta:
        model = Recipe
        exclude = ['author', 'is_approved', 'date_created']
        labels = {'image': 'Recipe image',
                  'ingredients': 'Ingredients and Their Quantity'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].widget = FileInput(attrs={'accept': 'image/*'})
        self.fields['ingredients'].widget = Textarea(
            attrs={'placeholder': 'Quantity Ingredient\n10g sugar'})
        self.fields['steps'].widget = Textarea(
            attrs={'placeholder': 'Step 1 - ...\nStep 2 - ...'})


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['rating', 'body']

        labels = {
            'body': 'Add a comment',
        }