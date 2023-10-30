from django.shortcuts import render, redirect
from django.contrib import messages

from recipes.forms import NewRecipe
from recipes.models import Recipe


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
    content = {'recipe': specific_recipe}
    return render(request, 'recipes/specific-recipe.html', content)
