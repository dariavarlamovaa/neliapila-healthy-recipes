from django.shortcuts import render


def get_recipes(request):
    return render(request, 'home/home.html')

