# Generated by Django 5.1.3 on 2024-11-18 13:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testpril', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='tournament',
            name='player_count',
            field=models.IntegerField(default=0),
        ),
    ]
