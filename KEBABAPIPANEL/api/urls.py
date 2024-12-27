from django.urls import path
from .views import RegisterUserView, LoginUserView, KebabListView, KebabDetailView

urlpatterns = [
    path('register_user', RegisterUserView.as_view(), name='register_user'),
    path('login_user', LoginUserView.as_view(), name='login_user'),
    path('kebabs', KebabListView.as_view(), name='kebab_list'),
    path('kebabs/<int:id>', KebabDetailView.as_view(), name='kebab_detail'),
]
