from django.db.models import Q

from recipes.models import Recipe


def get_sorted_recipes(request):
    sort_query = request.GET.get('sort_by') \
        if request.GET.get('sort_by') else ''
    if sort_query == 'All':
        recipes = Recipe.objects.filter(is_approved=True)
    else:
        recipes = Recipe.objects.filter(is_approved=True, category__iexact=sort_query)
    return recipes, sort_query


def get_found_recipes(request):
    search_query = request.GET.get('search-bar') \
        if request.GET.get('search-bar') else ''
    recipes = Recipe.objects.distinct().filter(Q(is_approved=True) &
                                               (Q(title__icontains=search_query) |
                                                Q(ingredients__icontains=search_query)))

    return recipes, search_query
