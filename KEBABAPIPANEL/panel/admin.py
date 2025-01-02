from django.contrib import admin
from api.models import Kebab

@admin.register(Kebab)
class KebabAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'opening_hours']
    search_fields = ['name', 'status']
    fields = ['name', 'description', 'latitude', 'longitude', 'opening_hours',
              'contact', 'meats', 'sauces', 'status', 'craft_rating',
              'order_methods', 'location_details', 'social_links']
