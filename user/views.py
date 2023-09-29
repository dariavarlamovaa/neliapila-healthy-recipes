from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError


def signup_user(request):
    if request.method == 'GET':
        return render(request, 'user/signup.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'user/signup.html',
                              {'error': 'User with this name already exists'})
        else:
            return render(request, 'user/signup.html',
                          {'error': 'Passwords are not the same'})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'user/login.html',
                          {'error': 'Invalid login information'})
        else:
            login(request, user)
            return redirect('home')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
