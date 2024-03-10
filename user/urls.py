from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from .views import RegisterView, UserLoginView, UserLogoutView, AuthorProfileView, MessagesView, FavoritesView

urlpatterns = [
    # login, signup, logout
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # favorites
    path('profile/favorites', FavoritesView.as_view(), name='favorites'),
    path('add-to-favorites/<pk>', views.add_recipe_to_favorites, name='add-to-favorites'),
    path('delete-from-favorites/<pk>', views.delete_favorite, name='delete-from-favorites'),

    # author(user) profile
    path('profile/<pk>', AuthorProfileView.as_view(), name='profile'),
    # edit profile info
    path('profile/<pk>/edit', views.edit_profile, name='edit-profile'),

    # contact
    path('contact-us/', views.contact_view, name='contact-us'),
    path('messages/', MessagesView.as_view(), name='messages'),

    # reset password
    path('password-reset/', PasswordResetView.as_view(template_name='user/password_reset.html'),
         name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),
         name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
