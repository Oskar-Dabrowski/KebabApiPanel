from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
import json

class Kebab(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def clean(self):
        if self.latitude < -90 or self.latitude > 90:
            raise ValidationError('Latitude must be between -90 and 90')
        if self.longitude < -180 or self.longitude > 180:
            raise ValidationError('Longitude must be between -180 and 180')
        if self.status not in dict(self.STATUS_CHOICES):
            raise ValidationError('Invalid status')

    contact = models.CharField(max_length=20, blank=True, null=True)
    meats = models.TextField(blank=True, null=True)
    sauces = models.TextField(blank=True, null=True)

    STATUS_CHOICES = [
    ('open', 'Open'),
    ('closed', 'Closed'),
    ('planned', 'Planned')
]
    status = models.CharField(
    max_length=50,
    choices=STATUS_CHOICES
)
    
    craft_rating = models.BooleanField(default=False)
    in_chain = models.BooleanField(default=False)
    order_methods = models.TextField(blank=True, null=True)
    location_details = models.TextField(blank=True, null=True)
    social_links = models.JSONField(blank=True, null=True)
    logo = models.ImageField(upload_to='kebab_logos/', blank=True, null=True)
    google_rating = models.FloatField(default=0)
    pyszne_rating = models.FloatField(default=0)
    last_updated = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.openinghour_set.exists():
            from api.models import OpeningHour
            default_hours = {
                "monday": {"open": "10:00", "close": "22:00"},
                "tuesday": {"open": "10:00", "close": "22:00"},
                "wednesday": {"open": "10:00", "close": "22:00"},
                "thursday": {"open": "10:00", "close": "22:00"},
                "friday": {"open": "10:00", "close": "23:00"},
                "saturday": {"open": "10:00", "close": "23:00"},
                "sunday": {"open": "10:00", "close": "20:00"}
            }
            OpeningHour.objects.create(kebab=self, hours=default_hours)

    def __str__(self):
        return self.name

class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kebab = models.ForeignKey(Kebab, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.kebab.name}"

def default_hours():
    return {
    "monday": {"open": "10:00", "close": "22:00"},
    "tuesday": {"open": "10:00", "close": "22:00"},
    "wednesday": {"open": "10:00", "close": "22:00"},
    "thursday": {"open": "10:00", "close": "22:00"},
    "friday": {"open": "10:00", "close": "23:00"},
    "saturday": {"open": "10:00", "close": "23:00"},
    "sunday": {"open": "10:00", "close": "20:00"}
}

class OpeningHour(models.Model):
    kebab = models.ForeignKey(Kebab, on_delete=models.CASCADE, related_name='openinghour_set')
    hours = models.JSONField(blank=True, null=True, default=default_hours, verbose_name="Godziny otwarcia")

    def save(self, *args, **kwargs):
        # Delete existing hours for the kebab before saving new ones
        OpeningHour.objects.filter(kebab=self.kebab).delete()
        super().save(*args, **kwargs)

    def clean(self):
    # Validation for empty or invalid times
        try:
            json.dumps(self.hours)  # Load JSON
        except TypeError:
            raise ValidationError("Hours must be a valid JSON object")

        # Existing validation logic
        required_days = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
        if set(self.hours.keys()) != required_days:
            raise ValidationError("Hours must contain all days of the week.")

        for day, schedule in self.hours.items():
            if not isinstance(schedule, dict) or 'open' not in schedule or 'close' not in schedule:
                raise ValidationError(f"Each day must have 'open' and 'close' times defined. Error in {day}.")
            if schedule['open'] and schedule['close']:
                if not isinstance(schedule['open'], str) or not isinstance(schedule['close'], str):
                    raise ValidationError(f"'open' and 'close' must be strings for {day}.")

    def __str__(self):
        return f"{self.kebab.name} - {self.hours}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kebab = models.ForeignKey(Kebab, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    
    def __str__(self):
        return f"{self.user.username} - {self.kebab.name}"

    class Meta:
        unique_together = ('user', 'kebab')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_changed_password = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def needs_password_change(self):
        return not self.has_changed_password

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

    def __str__(self):
        return f"{self.title} - {self.kebab.name}"

    def mark_as_accepted(self):
        self.status = 'Accepted'
        self.save()

    def mark_as_rejected(self):
        self.status = 'Rejected'
        self.save()
