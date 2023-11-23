from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # login, signup, logout
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup_user, name='signup'),
    path('logout/', views.logout_user, name='logout'),

    # favorites
    path('profile/favorites', views.get_favorites, name='favorites'),
    path('add-to-favorites/<pk>', views.add_recipe_to_favorites, name='add-to-favorites'),
    path('delete-from-favorites/<pk>', views.delete_favorite, name='delete-from-favorites'),

    # author(user) profile
    path('profile/<pk>', views.author_profile, name='profile'),
    # edit profile info
    path('profile/<pk>/edit', views.edit_profile, name='edit-profile'),

    # contact
    path('contact-us/', views.contact_view, name='contact-us'),
    path('messages/', views.get_messages, name='messages')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
