from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('emojis/', views.emoji_catalog, name='emoji_catalog'),
    path('favorites/', views.favorites, name='favorites'),
    path('toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='emoji_app/login.html'), name='login'),
]
