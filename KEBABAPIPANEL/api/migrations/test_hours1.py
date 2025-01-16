from django.db import migrations
import json

def set_hours(apps, schema_editor):
    Kebab = apps.get_model('api', 'Kebab')
    OpeningHour = apps.get_model('api', 'OpeningHour')

    kebab = Kebab.objects.get(name='test')

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
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_hours),
    ]