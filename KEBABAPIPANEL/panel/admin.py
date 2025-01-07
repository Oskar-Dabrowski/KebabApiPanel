from django.contrib import admin
from api.models import Kebab, Suggestion
from django.shortcuts import redirect
from django.urls import reverse

@admin.register(Kebab)

class KebabAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'opening_hours']
    search_fields = ['name', 'status']
    fields = ['name', 'description', 'latitude', 'longitude', 'opening_hours',
              'contact', 'meats', 'sauces', 'status', 'craft_rating',
              'order_methods', 'location_details', 'social_links']

    def has_change_permission(self, request, obj=None):
        if request.user.userprofile.has_changed_password == False:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.userprofile.has_changed_password == False:
            return False
        return super().has_delete_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        if request.user.userprofile.has_changed_password == False:
            return False
        return super().has_view_permission(request, obj)

    def changelist_view(self, request, extra_context=None):
        if request.user.userprofile.has_changed_password == False:
            return redirect(reverse('admin:password_change'))
        return super().changelist_view(request, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.user.userprofile.has_changed_password == False:
            return redirect(reverse('admin:password_change'))
        return super().change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        if request.user.userprofile.has_changed_password == False:
            return redirect(reverse('admin:password_change'))
        return super().add_view(request, form_url, extra_context)
    
    def response_change(self, request, obj):
        if request.user.userprofile.has_changed_password == False:
            request.user.userprofile.has_changed_password = True
            request.user.userprofile.save()
        return super().response_change(request, obj)

    def response_add(self, request, obj, post_url_continue=None):
        if request.user.userprofile.has_changed_password == False:
            request.user.userprofile.has_changed_password = True
            request.user.userprofile.save()
        return super().response_add(request, obj, post_url_continue)
    
@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ['user', 'kebab', 'suggestion', 'created_at']
    search_fields = ['user__username', 'kebab__name']