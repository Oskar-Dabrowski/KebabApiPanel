from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import (
    kebab_list_view,
    kebab_detail,
    check_suggestions,
    add_suggestion,
    get_favorites,
    bulk_opening_hours,
)

# Namespace for app-specific URLs
app_name = 'panel'

urlpatterns = [
    # Home and kebab-related endpoints
    path('', kebab_list_view, name='kebab_list'),
    path('kebabs/', kebab_list_view, name='kebab_list'),
    path('kebabs/<int:pk>/', kebab_detail, name='kebab_detail'),

    # Admin and authentication-related paths
    path('admin/', admin.site.urls, name='admin'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Suggestion-related endpoints
    path('check_suggestions/', check_suggestions, name='check_suggestions'),
    path('add_suggestion/', add_suggestion, name='add_suggestion'),

    # Favorites and bulk management
    path('favorites/', get_favorites, name='favorites'),
    path('opening_hours/bulk/', bulk_opening_hours, name='bulk_opening_hours'),
]
