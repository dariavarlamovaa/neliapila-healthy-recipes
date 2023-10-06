from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup_user, name='signup'),
    path('logout/', views.logout_user, name='logout'),

    path('profile/<pk>/my', views.get_profile, name='profile')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
