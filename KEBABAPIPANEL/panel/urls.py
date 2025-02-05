from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import (
    add_user_comment,
    kebab_list_view,
    kebab_detail,
    check_suggestions,
    add_suggestion,
    get_favorites,
    bulk_opening_hours,
    accept_suggestion,
    reject_suggestion,
    edit_hours,
    KebabHoursPanelView,  # Import the new view
)

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
    path('accept_suggestion/<int:suggestion_id>/', accept_suggestion, name='accept_suggestion'),
    path('reject_suggestion/<int:suggestion_id>/', reject_suggestion, name='reject_suggestion'),

    # Favorites and bulk management
    path('favorites/', get_favorites, name='favorites'),
    path('opening_hours/bulk/', bulk_opening_hours, name='bulk_opening_hours'),
    path('kebabs/<int:kebab_id>/edit_hours/', edit_hours, name='edit_hours'),

    # New endpoint for kebab hours
    path('kebab-hours/', KebabHoursPanelView, name='kebab_hours'),  # Add the new route

    path('kebabs/<int:kebab_id>/comment', add_user_comment, name='add_user_comment'),
]
