from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from .forms import NewUserCreationForm


def signup_user(request):
    form = NewUserCreationForm()
    if request.method == 'POST':
        form = NewUserCreationForm(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower().strip()
                user.save()
                messages.success(request, 'User account was created')
                login(request, user)
                return redirect('home')
    return render(request, 'user/signup.html', {'form': form})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            error = 'Invalid username or password'
            return render(request, 'user/login.html', {'error': error})
        else:
            login(request, user)
            return redirect('home')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
