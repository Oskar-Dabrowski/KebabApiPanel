# Generated by Django 4.2.5 on 2025-01-21 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_kebab_pyszne_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kebab',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
