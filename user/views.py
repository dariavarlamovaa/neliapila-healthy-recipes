from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate

from recipes.models import Recipe
from .forms import NewUserCreationForm, ProfileForm, ContactForm
from .models import Profile, Favorite, Contact


def signup_user(request):
    form = NewUserCreationForm()
    if request.method == 'POST':
        form = NewUserCreationForm(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            if form.is_valid():
                user = form.save(commit=False)
                if len(user.username) > 15:
                    messages.error(request, 'Username cannot contain more than 15 characters')
                else:
                    user.username = user.username.lower().strip()
                    user.first_name = user.first_name.strip()
                    user.last_name = user.last_name.strip()
                    user.email = user.email.lower().strip()
                    user.save()
                    messages.success(request, 'User account successfully created')
                    login(request, user)
                    return redirect('recipes')
    return render(request, 'user/signup.html', {'form': form})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is None:
            error = 'Invalid username or password'
            return render(request, 'user/login.html', {'error': error})
        else:
            login(request, user)
            return redirect('recipes')


@login_required(login_url='login')
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You were logged out')
        return redirect('recipes')


def author_profile(request, pk):
    profile = Profile.objects.get(user=pk)
    if request.user == profile.user or request.user.is_staff:
        recipes = Recipe.objects.filter(author=pk).all().order_by('-date_created')
    else:
        recipes = Recipe.objects.filter(author=pk, is_approved=True).all().order_by('-date_created')
    recipes_count = recipes.count()
    try:
        favorite_recipes = [favorite.favorite_recipe for favorite in request.user.profile.favorite_set.all()]
    except AttributeError:
        favorite_recipes = ''
    pending_recipes_count = Recipe.objects.filter(author=pk, is_approved=False).count()
    context = {'profile': profile, 'recipes': recipes, 'recipes_count': recipes_count,
               'pending_recipes_count': pending_recipes_count, 'favorites': favorite_recipes}
    return render(request, 'user/profile.html', context)


@login_required(login_url='login')
def edit_profile(request, pk):
    profile = Profile.objects.get(user=request.user.pk)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            edition = form.save(commit=False)
            edition.username = edition.username.lower().strip()
            edition.save()
            messages.success(request, 'Profile edited successfully')
            return redirect('profile', request.user.id)
        else:
            email_error = form.errors.get('email')
            username_error = form.errors.get('username')
            if form.errors.get('username'):
                messages.error(request, *username_error)
            if form.errors.get('email'):
                messages.error(request, *email_error)
    context = {'form': form, 'profile': profile}
    return render(request, 'user/profile-form.html', context)


@login_required(login_url='login')
def get_favorites(request):
    profile = Profile.objects.get(user=request.user.id)
    favorite_recipes = profile.favorite_set.all()
    favorite_recipes = [favorite.favorite_recipe for favorite in favorite_recipes]
    context = {'favorites': favorite_recipes}
    return render(request, 'user/favorites.html', context)


@login_required(login_url='login')
def add_recipe_to_favorites(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    if recipe.is_approved:
        favourite, created = Favorite.objects.get_or_create(
            favorite_recipe=recipe,
            profile=request.user.profile
        )
        if not created:
            favourite.save()
        messages.success(request, 'Recipe added to favorites')
        return redirect('favorites')


@login_required(login_url='login')
def delete_favorite(request, pk):
    favourite = get_object_or_404(Favorite, favorite_recipe_id=pk, profile=request.user.profile)
    if not request.user.id == favourite.profile.user.id:
        return HttpResponseForbidden('You do not have permission to access this page.')

    if request.method == 'GET':
        favourite.delete()
        messages.success(request, 'Recipe deleted from favorites')
        return redirect('favorites')


def contact_view(request):
    if request.user.is_authenticated:
        form = ContactForm(authenticated=True)
        sender = request.user.profile
    else:
        form = ContactForm()
        sender = None

    if request.method == 'POST':
        form = ContactForm(request.POST, authenticated=request.user.is_authenticated)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            if sender:
                message.email = sender.email

            messages.success(request, 'Your message successfully sent')
            message.save()

            return redirect('recipes')
    context = {'form': form}
    return render(request, 'user/contact-form.html', context)


def get_messages(request):
    all_messages = Contact.objects.order_by('-created').all()
    context = {'all_messages': all_messages}
    return render(request, 'user/messages.html', context)
