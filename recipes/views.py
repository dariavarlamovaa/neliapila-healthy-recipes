import re

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import CreateView, DeleteView, TemplateView, FormView, DetailView
from xhtml2pdf import pisa
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.contrib import messages

from home.views import paginate
from recipes.forms import NewRecipe, CommentForm
from recipes.models import Recipe, Comment


class RecipeCreationView(CreateView):
    template_name = 'recipes/add_recipe.html'
    form_class = NewRecipe
    model = Recipe

    def form_valid(self, form):
        user_recipe = form.save(commit=False)
        user_recipe.author = self.request.user.profile
        user_recipe.title = user_recipe.title.lower().capitalize().strip()
        user_recipe.ingredients = re.sub(r'\n\s*\n', '\n', user_recipe.ingredients.strip())
        user_recipe.steps = re.sub(r'\n\s*\n', '\n', user_recipe.steps.strip())
        user_recipe.save()
        messages.success(self.request,
                         'The recipe has been added successfully. Wait for the admin\'s approval')
        return redirect('profile', self.request.user.profile.id)

    def form_invalid(self, form):
        return super().form_invalid(form)


class CommentAddingView(CreateView):
    template_name = 'specific-recipe'
    form_class = CommentForm
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        specific_recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        try:
            if request.user.profile == specific_recipe.author:
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


class CommentDeleterView(DeleteView):
    def get(self, request, *args, **kwargs):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        if request.user.profile.id == comment.owner.id or request.user.is_staff:
            comment.delete()
            messages.success(request, 'You have deleted your comment')
            return redirect('specific-recipe', pk=comment.recipe.id)
        else:
            return HttpResponseForbidden('You do not have permission to access this page.')


def count_recipe_average_rating(recipe_ratings):
    average_rating = round(sum(recipe_ratings) / len(recipe_ratings), 1)
    return average_rating


class SpecificRecipeView(TemplateView):
    template_name = 'recipes/specific-recipe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        specific_recipe = Recipe.objects.get(pk=self.kwargs['pk'], is_approved=True)
        recipe_ingredients = specific_recipe.ingredients.split('\n')
        recipe_ingredients = [ingredient.strip() for ingredient in recipe_ingredients if ingredient.strip()]
        recipe_steps = specific_recipe.steps.split('\n')
        recipe_steps = [step.strip() for step in recipe_steps if step.strip()]
        comments = Comment.objects.select_related('owner__user__profile').filter(recipe=specific_recipe,
                                                                                 is_approved=True)
        comments_count = comments.count()
        recipe_ratings = [comment.rating for comment in comments]
        if recipe_ratings:
            average_recipe_rating = count_recipe_average_rating(recipe_ratings)
        else:
            average_recipe_rating = ''
        try:
            favorite_recipes = [favorite.favorite_recipe for favorite in self.request.user.profile.favorite_set.all()]
        except AttributeError:
            favorite_recipes = ''
        form = CommentForm()
        context.update({'recipe': specific_recipe, 'comments_count': comments_count,
                        'favorites': favorite_recipes, 'ingredients': recipe_ingredients,
                        'steps': recipe_steps, 'form': form, 'comments': comments,
                        'average_recipe_rating': average_recipe_rating})
        return context


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


class RecipeDeleterView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        recipe_to_delete = Recipe.objects.select_related('author__user__profile').get(pk=self.kwargs['pk'])
        return render(request, 'recipes/delete.html', {'recipe': recipe_to_delete})

    def post(self, request, *args, **kwargs):
        recipe_to_delete = Recipe.objects.select_related('author__user__profile').get(pk=self.kwargs['pk'])
        if request.user.profile.id == recipe_to_delete.author.id or request.user.is_staff:
            recipe_to_delete.delete()
            messages.success(request, f'Recipe - "{recipe_to_delete.title}" successfully deleted')
            return redirect('profile', self.request.user.profile.id)
        else:
            return HttpResponseForbidden('You do not have permission to access this page.')


# Functions for Admin
class PendingRecipesView(TemplateView):
    template_name = 'recipes/pending-recipes.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden('You do not have permission to access this page.')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_pending_recipes = Recipe.objects.filter(is_approved=False).all()
        all_pending_recipes, paginator, custom_range = paginate(self.request, all_pending_recipes)
        context.update({'recipes': all_pending_recipes, 'paginator': paginator, 'custom_range': custom_range})
        return context


class PendingRecipeApprovalView(DetailView):
    form_class = NewRecipe
    model = Recipe
    template_name = 'recipes/one-pending-recipe.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden('You do not have permission to access this page.')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        return recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        form = NewRecipe(instance=recipe)
        if 'image' in form.fields:
            del form.fields['image']
        context.update({'form': form})
        return context

    def post(self, request, *args, **kwargs):
        recipe = self.get_object()
        try:
            form = NewRecipe(request.POST, instance=recipe)
            recipe.is_approved = True
            form.save()
            return redirect('pending-recipes')
        except ValueError:
            messages.error(request, 'Something went wrong')
            return redirect('pending-recipes')


class PendingCommentView(TemplateView):
    template_name = 'recipes/pending-comments.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden('You do not have permission to access this page.')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_pending_comments = Comment.objects.filter(is_approved=False).all()
        all_pending_comments, paginator, custom_range = paginate(self.request, all_pending_comments)
        context.update({'comments': all_pending_comments, 'paginator': paginator, 'custom_range': custom_range})
        return context


class CommentApprovalView(DetailView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden('You do not have permission to access this page.')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        return comment

    def get(self, request, *args, **kwargs):
        comment = self.object
        comment.is_approved = True
        comment.save()
        return redirect('pending-comments')
