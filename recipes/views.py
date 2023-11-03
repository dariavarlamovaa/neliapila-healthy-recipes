from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages

from recipes.forms import NewRecipe, CommentForm
from recipes.models import Recipe, Comment


def add_a_recipe(request):
    profile = request.user
    form = NewRecipe()
    if request.method == 'POST':
        form = NewRecipe(request.POST, request.FILES)
        if form.is_valid():
            user_recipe = form.save(commit=False)
            user_recipe.author = profile
            user_recipe.title = user_recipe.title.capitalize().strip()
            user_recipe.save()
            messages.success(request,
                             'The recipe has been added successfully. Wait for the admin\'s approval')
            return redirect('profile', request.user.id)
    content = {'form': form}
    return render(request, 'recipes/add_recipe.html', content)


def show_specific_recipe(request, pk):
    specific_recipe = Recipe.objects.get(pk=pk)
    recipe_ingredients = specific_recipe.ingredients.split('\n')
    recipe_steps = specific_recipe.steps.split('\n')
    comments_count = Comment.objects.filter(recipe=specific_recipe, is_approved=True).count()
    print(comments_count)
    try:
        favorite_recipes = [favorite.favorite_recipe for favorite in request.user.profile.favorite_set.all()]
    except AttributeError:
        favorite_recipes = ''
    form = CommentForm()
    try:
        if request.method == 'POST':
            if request.user.profile == specific_recipe.author.profile:
                messages.error(request, 'You can`t leave a comment on your own recipe')
                return redirect('specific-recipe', pk=specific_recipe.id)
            else:
                form = CommentForm(request.POST)
                comment = form.save(commit=False)
                comment.recipe = specific_recipe
                comment.owner = request.user.profile
                comment.save()

                messages.success(request, 'Your comment posted successfully')
                return redirect('specific-recipe', pk=specific_recipe.id)
    except IntegrityError:
        messages.error(request, 'You have already posted the comment')
        return redirect('specific-recipe', pk=specific_recipe.id)
    content = {'recipe': specific_recipe, 'comments_count': comments_count,
               'favorites': favorite_recipes, 'ingredients': recipe_ingredients,
               'steps': recipe_steps, 'form': form}
    return render(request, 'recipes/specific-recipe.html', content)
