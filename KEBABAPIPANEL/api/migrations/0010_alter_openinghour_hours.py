# Generated by Django 4.2.5 on 2025-01-15 15:31

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_openinghour_hours_alter_openinghour_kebab'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openinghour',
            name='hours',
            field=models.JSONField(default=api.models.default_hours),
        ),
    ]
