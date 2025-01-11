# api/urls.py
from django.urls import path
from .views import (
    RegisterUserView,
    LoginUserView,
    KebabListView,
    KebabDetailView,
    SuggestionView,
    SuggestionListView,
    AddFavoriteView,
    RemoveFavoriteView,
    AddUserCommentView,
)

urlpatterns = [
    # User-related endpoints
    path('register_user', RegisterUserView.as_view(), name='register_user'),
    path('login_user', LoginUserView.as_view(), name='login_user'),
    
    # Kebab-related endpoints
    path('kebabs', KebabListView.as_view(), name='kebab_list'),
    path('kebabs/<int:id>', KebabDetailView.as_view(), name='kebab_detail'),
    
    # Suggestion-related endpoints
    path('suggestions', SuggestionListView.as_view(), name='suggestion_list_create'),
    path('suggestions/<int:pk>', SuggestionView.as_view(), name='suggestion_detail'),
    
    # Favorites-related endpoints
    path('kebabs/<int:id>/favorite', AddFavoriteView.as_view(), name='add_favorite'),
    path('kebabs/<int:id>/unfavorite', RemoveFavoriteView.as_view(), name='remove_favorite'),

    # Comments-related endpoints
    path('kebabs/<int:id>/comment', AddUserCommentView.as_view(), name='add_user_comment'),
]
