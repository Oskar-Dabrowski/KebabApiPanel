from django.contrib import admin
from api.models import Kebab, OpeningHour, Suggestion, UserComment, UserProfile, Favorite
from django.shortcuts import redirect
from django.urls import reverse
import json
from django import forms

@admin.register(Kebab)
class KebabAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'google_rating', 'pyszne_rating', 'last_updated']
    search_fields = ['name', 'status', 'description', 'contact', 'meats', 'sauces', 'craft_rating', 'in_chain', 'order_methods', 'location_details', 'google_rating', 'pyszne_rating', 'last_updated']
    list_filter = ['name', 'status', 'description', 'contact', 'meats', 'sauces', 'craft_rating', 'in_chain', 'order_methods', 'location_details', 'google_rating', 'pyszne_rating', 'last_updated']

class JSONWidget(forms.Textarea):
    """
    Niestandardowy widget do edycji danych JSON w panelu administracyjnym.
    """
    def __init__(self, attrs=None):
        final_attrs = {'style': 'font-family: monospace;'}
        if attrs:
            final_attrs.update(attrs)
        super().__init__(final_attrs)

    def format_value(self, value):
        if isinstance(value, dict):  # Formatuj JSON w bardziej czytelny sposób
            import json
            return json.dumps(value, indent=2, ensure_ascii=False)
        return super().format_value(value)
    
class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['kebab', 'hours']
        widgets = {
            'hours': JSONWidget(attrs={'rows': 10, 'cols': 80}),
        }


@admin.register(OpeningHour)
class OpeningHourAdmin(admin.ModelAdmin):
    form = OpeningHourForm
    list_display = ['kebab', 'hours']  # Wyświetlaj kebab i godziny
    search_fields = ['kebab__name']

    def formatted_hours(self, obj):
        try:
            hours = json.loads(obj.hours)
            return f"Open: {hours.get('open', 'N/A')}, Close: {hours.get('close', 'N/A')}"
        except (ValueError, TypeError):
            return "Invalid JSON format"
    formatted_hours.short_description = "Formatted Hours"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['hours'].widget.attrs['placeholder'] = "{'monday': {'open': '10:00', 'close': '20:00'}, 'tuesday': {'open': '10:00', 'close': '20:00'}, ...}"
        return form
    
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['hours_template'] = "{'monday': {'open': '10:00', 'close': '20:00'}, 'tuesday': {'open': '10:00', 'close': '20:00'}, ...}"
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['hours_template'] = "{'monday': {'open': '10:00', 'close': '20:00'}, 'tuesday': {'open': '10:00', 'close': '20:00'}, ...}"
        return super().change_view(request, object_id, form_url, extra_context)

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
    search_fields = ('title', 'user__username', 'kebab__name', 'status', 'created_at')
    list_filter = ('user__username', 'kebab__name', 'status', 'created_at')

    def kebab_name(self, obj):
        return obj.kebab.name
    kebab_name.short_description = 'Kebab'
    kebab_name.admin_order_field = 'kebab__name'

@admin.register(UserComment)
class UserCommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'kebab_name', 'text', 'created_at')
    search_fields = ('user__username', 'kebab__name', 'text', 'created_at')
    list_filter = ('user', 'kebab', 'created_at')

    def user_name(self, obj):
        return obj.user.username
    user_name.short_description = 'User'
    user_name.admin_order_field = 'user__username'

    def kebab_name(self, obj):
        return obj.kebab.name
    kebab_name.short_description = 'Kebab'
    kebab_name.admin_order_field = 'kebab__name'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'has_changed_password')
    list_filter = ('has_changed_password',)
    search_fields = ('user__username',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'kebab_name', 'created_at')
    search_fields = ('user__username', 'kebab__name', 'created_at')
    list_filter = ('user', 'user__username', 'kebab__name', 'created_at')

    def user_name(self, obj):
        return obj.user.username
    user_name.short_description = 'User'
    user_name.admin_order_field = 'user__username'

    def kebab_name(self, obj):
        return obj.kebab.name
    kebab_name.short_description = 'Kebab'
    kebab_name.admin_order_field = 'kebab__name'