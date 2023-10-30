from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_recipes, name='recipes'),
    path('', include('user.urls'))
]
