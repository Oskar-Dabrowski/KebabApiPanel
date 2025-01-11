from django.urls import path, include
from django.contrib import admin
from .views import kebab_list_view
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', kebab_list_view, name='kebab_list'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('kebabs/', kebab_list_view, name='kebab_list'),
    path('kebabs/<int:pk>/', views.kebab_detail, name='kebab_detail'),
    path('admin/', admin.site.urls, name='password_change'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('check_suggestions/', views.check_suggestions, name='check_suggestions'),
    path('add_suggestion/', views.add_suggestion, name='add_suggestion'),
    path('kebabs/<int:pk>/favorite/', views.add_favorite, name='add_favorite'),
    path('kebabs/<int:pk>/unfavorite/', views.remove_favorite, name='remove_favorite'),
    path('kebabs/<int:pk>/comment/', views.add_user_comment, name='add_user_comment'),
]