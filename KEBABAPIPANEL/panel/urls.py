from django.urls import path
from .views import kebab_list_view, kebab_edit_view

urlpatterns = [
    path('kebabs/', kebab_list_view, name='kebab_list'),
    path('kebabs/edit/<int:id>/', kebab_edit_view, name='kebab_edit'),
]
