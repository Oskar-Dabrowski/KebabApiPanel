# Generated by Django 4.2.5 on 2025-01-17 11:55

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_favorite_kebab_alter_favorite_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openinghour',
            name='hours',
            field=models.JSONField(blank=True, default=api.models.default_hours, null=True, verbose_name='Godziny otwarcia'),
        ),
    ]
