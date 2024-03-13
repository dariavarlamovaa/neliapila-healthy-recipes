from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView, DeleteView

from recipes.models import Recipe
from .forms import NewUserCreationForm, ProfileForm, ContactForm
from .models import Profile, Favorite, Contact


class RegisterView(CreateView):
    form_class = NewUserCreationForm
    template_name = 'user/signup.html'
    success_url = reverse_lazy('recipes')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('recipes')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)

        user.username = form.cleaned_data['username'].lower().strip()
        user.email = form.cleaned_data['email'].lower().strip()

        user.set_password(form.cleaned_data['password1'])

        user.save()

        login(self.request, user)

        messages.success(self.request, 'User account successfully created')
        return redirect('recipes')

    def form_invalid(self, form):
        return super().form_invalid(form)


class UserLoginView(View):
    template_name = 'user/login.html'

    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is None:
            error = 'Invalid username or password'
            return render(request, 'user/login.html', {'error': error})
        else:
            login(request, user)
            return redirect('recipes')


class UserLogoutView(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('recipes')


class AuthorProfileView(DetailView):
    model = Profile
    template_name = 'user/profile.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        author_id = profile.id
        if self.request.user == profile.user or self.request.user.is_staff:
            recipes = Recipe.objects.filter(author=author_id).all().order_by('-date_created')
        else:
            recipes = Recipe.objects.filter(author=author_id, is_approved=True).all().order_by('-date_created')
        recipes_count = recipes.count()
        try:
            favorite_recipes = [favorite.favorite_recipe for favorite in self.request.user.profile.favorite_set.all()]
        except AttributeError:
            favorite_recipes = ''
        pending_recipes_count = Recipe.objects.filter(author=author_id, is_approved=False).count()

        context.update({
            'recipes': recipes,
            'recipes_count': recipes_count,
            'pending_recipes_count': pending_recipes_count,
            'favorites': favorite_recipes,
        })
        return context


class ProfileEditorView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'user/profile-form.html'
    pk_url_kwarg = 'pk'
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        edition = form.save(commit=False)
        edition.username = edition.username.lower().strip()
        edition.save()
        messages.success(self.request, 'Profile edited successfully')
        return redirect('profile', self.request.user.profile.id)

    def form_invalid(self, form):
        email_error = form.errors.get('email')
        username_error = form.errors.get('username')
        if form.errors.get('username'):
            messages.error(self.request, *username_error)
        if form.errors.get('email'):
            messages.error(self.request, *email_error)


class FavoritesView(LoginRequiredMixin, TemplateView):
    template_name = 'user/favorites.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        profile = Profile.objects.get(user=self.request.user.id)
        favorite_recipes = profile.favorite_set.all()
        favorite_recipes = [favorite.favorite_recipe for favorite in favorite_recipes]
        context.update({'favorites': favorite_recipes})
        return context


class FavoriteAddingView(LoginRequiredMixin, View):
    model = Favorite

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if recipe.is_approved:
            favourite, created = self.model.objects.get_or_create(
                favorite_recipe=recipe,
                profile=request.user.profile
            )
            if not created:
                favourite.save()
            messages.success(request, 'Recipe added to favorites')
            return redirect('favorites')


class FavoriteDeleterView(LoginRequiredMixin, View):
    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, pk):
        favourite = get_object_or_404(Favorite, favorite_recipe_id=pk, profile=request.user.profile)
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


class MessagesView(TemplateView):
    template_name = 'user/messages.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden('You do not have permission to access this page.')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        all_messages = Contact.objects.order_by('-created').all()
        context.update({'all_messages': all_messages})
        return context
