from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

class Kebab(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    contact = models.CharField(max_length=20, blank=True, null=True)
    meats = models.TextField(blank=True, null=True)
    sauces = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=50,
        choices=[('open', 'Open'), ('closed', 'Closed'), ('planned', 'Planned')]
    )
    craft_rating = models.BooleanField(default=False)
    in_chain = models.BooleanField(default=False)
    order_methods = models.TextField(blank=True, null=True)
    location_details = models.TextField(blank=True, null=True)
    social_links = models.JSONField(blank=True, null=True)
    logo = models.ImageField(upload_to='kebab_logos/', blank=True, null=True)
    google_rating = models.FloatField(blank=True, null=True)
    pyszne_rating = models.FloatField(blank=True, null=True)
    last_updated = models.DateTimeField(default=now)

class UserComment(models.Model):
    kebab = models.ForeignKey(Kebab, on_delete=models.CASCADE, related_name="comments")
    user_name = models.CharField(max_length=255)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class OpeningHour(models.Model):
    kebab = models.ForeignKey(Kebab, on_delete=models.CASCADE, related_name="opening_hours")
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('monday', 'Monday'),
            ('tuesday', 'Tuesday'),
            ('wednesday', 'Wednesday'),
            ('thursday', 'Thursday'),
            ('friday', 'Friday'),
            ('saturday', 'Saturday'),
            ('sunday', 'Sunday'),
        ]
    )
    open_time = models.TimeField()
    close_time = models.TimeField()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_changed_password = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suggestions')
    kebab = models.ForeignKey(Kebab, on_delete=models.CASCADE, related_name='suggestions')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Accepted', 'Accepted'),
            ('Rejected', 'Rejected'),
        ],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    