import re

from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.contrib import messages

from recipes.forms import NewRecipe, CommentForm
from recipes.models import Recipe, Comment


@login_required(login_url='login')
def add_a_recipe(request):
    profile = request.user
    form = NewRecipe()
    if request.method == 'POST':
        form = NewRecipe(request.POST, request.FILES)
        if form.is_valid():
            user_recipe = form.save(commit=False)
            user_recipe.author = profile
            user_recipe.title = user_recipe.title.lower().capitalize().strip()
            user_recipe.ingredients = re.sub(r'\n\s*\n', '\n', user_recipe.ingredients.strip())
            user_recipe.steps = re.sub(r'\n\s*\n', '\n', user_recipe.steps.strip())
            user_recipe.save()
            messages.success(request,
                             'The recipe has been added successfully. Wait for the admin\'s approval')
            return redirect('profile', request.user.id)
    context = {'form': form}
    return render(request, 'recipes/add_recipe.html', context)


def leave_a_comment(request, specific_recipe):
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

                messages.success(request, 'Your comment posted successfully. Wait for the admin\'s approval')
                return redirect('specific-recipe', pk=specific_recipe.id)
    except IntegrityError:
        messages.error(request, 'You have already posted the comment')
        return redirect('specific-recipe', pk=specific_recipe.id)


def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    if not request.user.id == comment.owner.id:
        return HttpResponseForbidden('You do not have permission to access this page.')
    if request.method == 'GET':
        comment.delete()
        messages.success(request, 'You have deleted your comment')
        return redirect('specific-recipe', pk=comment.recipe.id)


def show_specific_recipe(request, pk):
    specific_recipe = Recipe.objects.get(pk=pk, is_approved=True)
    recipe_ingredients = specific_recipe.ingredients.split('\n')
    recipe_ingredients = [ingredient.strip() for ingredient in recipe_ingredients if ingredient.strip()]
    recipe_steps = specific_recipe.steps.split('\n')
    recipe_steps = [step.strip() for step in recipe_steps if step.strip()]
    comments = Comment.objects.filter(recipe=specific_recipe, is_approved=True)
    comments_count = comments.count()
    recipe_ratings = [comment.rating for comment in comments]
    if recipe_ratings:
        average_recipe_rating = round(sum(recipe_ratings) / len(recipe_ratings), 1)
    else:
        average_recipe_rating = ''
    try:
        favorite_recipes = [favorite.favorite_recipe for favorite in request.user.profile.favorite_set.all()]
    except AttributeError:
        favorite_recipes = ''
    form = CommentForm()
    if request.method == 'POST':
        leave_a_comment(request, specific_recipe)
    context = {'recipe': specific_recipe, 'comments_count': comments_count,
               'favorites': favorite_recipes, 'ingredients': recipe_ingredients,
               'steps': recipe_steps, 'form': form, 'comments': comments,
               'average_recipe_rating': average_recipe_rating}
    return render(request, 'recipes/specific-recipe.html', context)


def get_pdf(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    context = {
        'recipe': recipe,
        'ingredients': recipe.ingredients.split('\n'),
        'steps': recipe.steps.split('\n'),
    }

    template = get_template('recipes/for-pdf.html')
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=recipe_{pk}.pdf'

    pisa_status = pisa.CreatePDF(
        html, dest=response
    )

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


@login_required(login_url='login')
def delete_recipe(request, pk):
    recipe_to_delete = Recipe.objects.get(pk=pk)

    if not request.user.id == recipe_to_delete.author.id:
        return HttpResponseForbidden('You do not have permission to access this page.')

    if request.method == 'POST':
        recipe_to_delete.delete()
        messages.success(request, f'Recipe - "{recipe_to_delete.title}" successfully deleted')
        return redirect('profile', request.user.id)

    context = {'recipe': recipe_to_delete}
    return render(request, 'recipes/delete.html', context)
