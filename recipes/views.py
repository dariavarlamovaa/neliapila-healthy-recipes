import re

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.contrib import messages

from home.views import paginate
from recipes.forms import NewRecipe, CommentForm
from recipes.models import Recipe, Comment


@login_required
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
    if request.user.id == comment.owner.id or request.user.is_staff:
        if request.method == 'GET':
            comment.delete()
            messages.success(request, 'You have deleted your comment')
            return redirect('specific-recipe', pk=comment.recipe.id)
    else:
        return HttpResponseForbidden('You do not have permission to access this page.')


def count_recipe_average_rating(recipe_ratings):
    average_rating = round(sum(recipe_ratings) / len(recipe_ratings), 1)
    return average_rating


def show_specific_recipe(request, pk):
    specific_recipe = Recipe.objects.get(pk=pk, is_approved=True)
    recipe_ingredients = specific_recipe.ingredients.split('\n')
    recipe_ingredients = [ingredient.strip() for ingredient in recipe_ingredients if ingredient.strip()]
    recipe_steps = specific_recipe.steps.split('\n')
    recipe_steps = [step.strip() for step in recipe_steps if step.strip()]
    comments = Comment.objects.select_related('owner__user__profile').filter(recipe=specific_recipe, is_approved=True)
    comments_count = comments.count()
    recipe_ratings = [comment.rating for comment in comments]
    if recipe_ratings:
        average_recipe_rating = count_recipe_average_rating(recipe_ratings)
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


@login_required
def delete_recipe(request, pk):
    recipe_to_delete = Recipe.objects.get(pk=pk)

    if request.user.id == recipe_to_delete.author.id or request.user.is_staff:
        if request.method == 'POST':
            recipe_to_delete.delete()
            messages.success(request, f'Recipe - "{recipe_to_delete.title}" successfully deleted')
            return redirect('profile', request.user.id)
    else:
        return HttpResponseForbidden('You do not have permission to access this page.')

    context = {'recipe': recipe_to_delete}
    return render(request, 'recipes/delete.html', context)


@staff_member_required
def pending_recipes(request):
    all_pending_recipes = Recipe.objects.filter(is_approved=False).all()
    all_pending_recipes, paginator, custom_range = paginate(request, all_pending_recipes)
    context = {'recipes': all_pending_recipes, 'paginator': paginator, 'custom_range': custom_range}
    return render(request, 'recipes/pending-recipes.html', context)


@staff_member_required
def approve_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    form = NewRecipe(instance=recipe)
    if 'image' in form.fields:
        del form.fields['image']
    if request.method == 'GET':
        return render(request, 'recipes/one-pending-recipe.html',
                      {'recipe': recipe, 'form': form})
    else:
        try:
            form = NewRecipe(request.POST, instance=recipe)
            recipe.is_approved = True
            form.save()
            return redirect('pending-recipes')
        except ValueError:
            messages.error(request, 'Something went wrong')
            return render(request, 'recipes/one-pending-recipe.html',
                          {'form': form})


@staff_member_required
def pending_comments(request):
    all_pending_comments = Comment.objects.filter(is_approved=False).all()
    all_pending_comments, paginator, custom_range = paginate(request, all_pending_comments)
    if request.method == 'GET':
        context = {'comments': all_pending_comments, 'paginator': paginator, 'custom_range': custom_range}
        return render(request, 'recipes/pending-comments.html', context)


@staff_member_required
def approve_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    print(comment)
    if request.method == 'GET':
        comment.is_approved = True
        comment.save()
        return redirect('pending-comments')
