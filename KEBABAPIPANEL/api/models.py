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

    def __str__(self):
        return self.name


class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kebab = models.ForeignKey(Kebab, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.kebab.name}"

class OpeningHour(models.Model):
    kebab = models.ForeignKey(Kebab, on_delete=models.CASCADE, related_name='openinghour_set')
    hours = models.JSONField(default={
        'monday': {'open': '00:00', 'close': '00:00'},
        'tuesday': {'open': '00:00', 'close': '00:00'},
        'wednesday': {'open': '00:00', 'close': '00:00'},
        'thursday': {'open': '00:00', 'close': '00:00'},
        'friday': {'open': '00:00', 'close': '00:00'},
        'saturday': {'open': '00:00', 'close': '00:00'},
        'sunday': {'open': '00:00', 'close': '00:00'}
    })  # Użyj JSONField do przechowywania godzin

    def clean(self):
        # Walidacja formatu JSON
        try:
            parsed_hours = json.loads(self.hours)  # Załaduj JSON
        except json.JSONDecodeError:
            raise ValidationError("Hours must be valid JSON.")

        # Walidacja struktury JSON
        required_days = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
        if set(parsed_hours.keys()) != required_days:
            raise ValidationError("Hours must contain all days of the week.")

        for day, schedule in parsed_hours.items():
            if not isinstance(schedule, dict) or 'open' not in schedule or 'close' not in schedule:
                raise ValidationError(f"Each day must have 'open' and 'close' times defined. Error in {day}.")
            if schedule['open'] and schedule['close']:
                # Sprawdź, czy format godzin jest poprawny (opcjonalnie)
                if not isinstance(schedule['open'], str) or not isinstance(schedule['close'], str):
                    raise ValidationError(f"'open' and 'close' must be strings for {day}.")

    def __str__(self):
        return f"{self.kebab.name} - {self.hours}"  # Display kebab name and hours

    def clean(self):
        import datetime

        valid_days = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
        if not isinstance(self.hours, dict):
            raise ValidationError("Opening hours must be a JSON object.")
        
        for day, times in self.hours.items():
            if day not in valid_days:
                raise ValidationError(f"Invalid day: {day}")
            if "open" not in times or "close" not in times:
                raise ValidationError(f"Invalid format for {day}. Use {'open': ..., 'close': ...}.")
            try:
                datetime.datetime.strptime(times["open"], "%H:%M")
                datetime.datetime.strptime(times["close"], "%H:%M")
            except ValueError:
                raise ValidationError(f"Invalid time format for {day}. Use HH:MM.")

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
