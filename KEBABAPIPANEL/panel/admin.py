from django.contrib import admin
from api.models import Kebab

@admin.register(Kebab)
class KebabAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'opening_hours']
    search_fields = ['name', 'status']
