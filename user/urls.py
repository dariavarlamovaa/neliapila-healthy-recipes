from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # login, signup, logout
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup_user, name='signup'),
    path('logout/', views.logout_user, name='logout'),

    # author(user) profile
    path('profile/<pk>', views.author_profile, name='profile'),
    # edit profile info
    path('profile/<pk>/edit', views.edit_profile, name='edit-profile')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
