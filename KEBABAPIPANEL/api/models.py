from django.db import models

class Kebab(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    opening_hours = models.CharField(max_length=255)
    contact = models.CharField(max_length=20, blank=True, null=True)
    meats = models.TextField(blank=True, null=True)
    sauces = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=50,
        choices=[('open', 'Open'), ('closed', 'Closed'), ('planned', 'Planned')]
    )
    craft_rating = models.BooleanField(default=False)
    order_methods = models.TextField(blank=True, null=True)
    location_details = models.TextField(blank=True, null=True)
    social_links = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name
