from django.contrib import admin
from api.models import Kebab, OpeningHour, Suggestion
from django.shortcuts import redirect
from django.urls import reverse

@admin.register(Kebab)
class KebabAdmin(admin.ModelAdmin):
    list_display = ['name', 'status']
    search_fields = ['name', 'status']
    fields = ['name', 'description', 'latitude', 'longitude',
              'contact', 'meats', 'sauces', 'status', 'craft_rating', 'in_chain', 
              'order_methods', 'location_details', 'social_links', 'logo', 'google_rating', 'pyszne_rating', 'last_updated']

@admin.register(OpeningHour)
class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ['kebab_name', 'day_of_week', 'open_time', 'close_time']
    search_fields = ['kebab__name', 'day_of_week']
    list_filter = ['kebab__name', 'day_of_week']

    def kebab_name(self, obj):
        return obj.kebab.name
    kebab_name.short_description = 'Kebab'
    kebab_name.admin_order_field = 'kebab__name'

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
    list_display = ('title', 'user', 'kebab_name', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'user__username', 'kebab__name')

    def kebab_name(self, obj):
        return obj.kebab.name
    kebab_name.short_description = 'Kebab'
    kebab_name.admin_order_field = 'kebab__name'