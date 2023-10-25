from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from recipes.models import Recipe
from .forms import NewUserCreationForm, ProfileForm
from .models import Profile


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
                    return redirect('home')
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
            return redirect('home')


@login_required(login_url='login')
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You were logged out')
        return redirect('home')


def author_profile(request, pk):
    profile = Profile.objects.get(user=pk)
    if request.user == profile.user:
        recipes = Recipe.objects.filter(author=pk).all().order_by('-date_created')
    else:
        recipes = Recipe.objects.filter(author=pk, is_approved=True).all().order_by('-date_created')
    recipes_count = recipes.count()
    pending_recipes_count = Recipe.objects.filter(author=pk, is_approved=False).count()
    context = {'profile': profile, 'recipes': recipes, 'recipes_count': recipes_count,
               'pending_recipes_count': pending_recipes_count}
    return render(request, 'user/profile.html', context)


@login_required(login_url='login')
def edit_profile(request, pk):
    profile = Profile.objects.get(user=request.user.pk)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile edited successfully')
            return redirect('profile', request.user.id)
        else:
            username_error = form.errors.get('username')
            if username_error:
                messages.error(request, *username_error)
    context = {'form': form, 'profile': profile}
    return render(request, 'user/profile-form.html', context)


@login_required(login_url='login')
def favorites(request):
    profile = Profile.objects.get(user=request.user.id)
    favorite_recipes = profile.favorite_set.all()
    favorite_recipes = [favorite.recipe for favorite in favorite_recipes]
    context = {'favorites': favorite_recipes}
    return render(request, 'user/favorites.html', context)
