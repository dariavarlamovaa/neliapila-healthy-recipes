from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import NewUserCreationForm
from .models import Profile


def signup_user(request):
    form = NewUserCreationForm()
    if request.method == 'POST':
        form = NewUserCreationForm(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            if form.is_valid():
                user = form.save(commit=False)
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


@login_required(login_url='login')
def get_profile(request, pk):
    profile = Profile.objects.get(user=request.user.pk)
    context = {'profile': profile}
    return render(request, 'user/profile.html', context)
