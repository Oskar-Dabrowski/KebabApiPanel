from django.urls import path, include
from django.contrib import admin
from .views import kebab_list_view, kebab_edit_view
from .views import custom_login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('kebabs/', kebab_list_view, name='kebab_list'),
    path('kebabs/edit/<int:id>/', kebab_edit_view, name='kebab_edit'),
    path('admin/', admin.site.urls, name='password_change'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
]