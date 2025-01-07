from django.urls import path
from .views import (
    kebab_list_view, kebab_edit_view, kebab_detail_view, kebab_edit_social_links,
    suggestion_list_view, suggestion_accept_view, suggestion_reject_view
)

urlpatterns = [
    path('kebabs/', kebab_list_view, name='kebab_list'),
    path('kebabs/edit/<int:id>/', kebab_edit_view, name='kebab_edit'),
    path('kebabs/<int:id>/', kebab_detail_view, name='kebab_detail'),
    path('kebabs/<int:id>/edit-social-links/', kebab_edit_social_links, name='kebab_edit_social_links'),
    path('suggestions/', suggestion_list_view, name='suggestion_list'),
    path('suggestions/accept/<int:id>/', suggestion_accept_view, name='suggestion_accept'),
    path('suggestions/reject/<int:id>/', suggestion_reject_view, name='suggestion_reject'),
]