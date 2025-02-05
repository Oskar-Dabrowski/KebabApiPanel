from django.contrib.auth.signals import user_logged_in 
from django.dispatch import receiver
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, Kebab, OpeningHour
from django.db.models.signals import post_save

@receiver(user_logged_in)
def force_password_change(sender, request, user, **kwargs):
    if user.userprofile.has_changed_password == False:
        return redirect(reverse('admin:password_change'))
    user.userprofile.has_changed_password = True
    user.userprofile.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user= instance)

@receiver(post_save, sender=User )
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=User)
def password_changed_handler(sender, instance, **kwargs):
    if kwargs.get('created', False):
        return
    if instance.userprofile.has_changed_password == False:
        instance.userprofile.has_changed_password = True
        instance.userprofile.save()

DEFAULT_OPENING_HOURS = {
    'monday': {'open': '00:00', 'close': '00:00'},
    'tuesday': {'open': '00:00', 'close': '00:00'},
    'wednesday': {'open': '00:00', 'close': '00:00'},
    'thursday': {'open': '00:00', 'close': '00:00'},
    'friday': {'open': '00:00', 'close': '00:00'},
    'saturday': {'open': '00:00', 'close': '00:00'},
    'sunday': {'open': '00:00', 'close': '00:00'}
}

@receiver(post_save, sender=Kebab)
def create_opening_hours(sender, instance, created, **kwargs):
    if created:
        OpeningHour.objects.create(kebab=instance, hours=DEFAULT_OPENING_HOURS)