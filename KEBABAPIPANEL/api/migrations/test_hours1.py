from django.db import migrations
import json

def set_hours(apps, schema_editor):
    Kebab = apps.get_model('api', 'Kebab')
    OpeningHour = apps.get_model('api', 'OpeningHour')

    # Create a test kebab if it doesn't exist
    kebab, created = Kebab.objects.get_or_create(name='test', defaults={
        'latitude': 51.2095,
        'longitude': 16.1554,
        'status': 'open'
    })

    hours = {
        "monday": {"open": "19:00", "close": "22:00"},
        "tuesday": {"open": "00:00", "close": "13:00"},
        "wednesday": {"open": "06:00", "close": "21:00"},
        "thursday": {"open": "19:00", "close": "20:00"},
        "friday": {"open": "13:00", "close": "22:00"},
        "saturday": {"open": "04:00", "close": "06:00"},
        "sunday": {"open": "21:00", "close": "22:00"}
    }

    OpeningHour.objects.update_or_create(
        kebab=kebab,
        defaults={'hours': str(hours).replace("'", "")}
    )

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_openinghour_hours'),
    ]

    operations = [
        migrations.RunPython(set_hours),
    ]
