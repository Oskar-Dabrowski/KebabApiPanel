# Generated by Django 4.2.5 on 2025-01-09 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_kebab_opening_hours_openinghour'),
    ]

    operations = [
        migrations.AddField(
            model_name='kebab',
            name='in_chain',
            field=models.BooleanField(default=False),
        ),
    ]
