from django.shortcuts import render, redirect
from django.contrib import messages

from recipes.forms import NewRecipe


def add_a_recipe(request):
    profile = request.user
    form = NewRecipe()
    if request.method == 'POST':
        form = NewRecipe(request.POST, request.FILES)
        if form.is_valid():
            user_recipe = form.save(commit=False)
            user_recipe.author = profile
            user_recipe.save()
            messages.success(request,
                             'The recipe has been added successfully. Wait for the admin\'s approval')
            return redirect('profile', request.user.id)

    content = {'form': form}
    return render(request, 'recipes/add_recipe.html', content)
