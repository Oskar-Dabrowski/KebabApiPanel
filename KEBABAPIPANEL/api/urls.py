from django.urls import path
from .views import (
    RegisterUserView,
    LoginUserView,
    KebabListView,
    KebabDetailView,
    SuggestionListCreateView,
    SuggestionDetailView,
)

urlpatterns = [
    # User-related endpoints
    path('register_user', RegisterUserView.as_view(), name='register_user'),
    path('login_user', LoginUserView.as_view(), name='login_user'),
    
    # Kebab-related endpoints
    path('kebabs', KebabListView.as_view(), name='kebab_list'),
    path('kebabs/<int:id>', KebabDetailView.as_view(), name='kebab_detail'),
    
    # Suggestion-related endpoints
    path('suggestions', SuggestionListCreateView.as_view(), name='suggestion_list_create'),
    path('suggestions/<int:pk>', SuggestionDetailView.as_view(), name='suggestion_detail'),
]
