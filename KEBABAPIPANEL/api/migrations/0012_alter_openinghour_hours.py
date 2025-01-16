# Generated by Django 4.2.5 on 2025-01-16 13:16

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_add_sample_opening_hours1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openinghour',
            name='hours',
            field=models.JSONField(blank=True, default=api.models.default_hours, null=True),
        ),
    ]
