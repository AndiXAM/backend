# Generated by Django 5.1.3 on 2024-11-18 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testpril', '0004_player_tournaments'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='max_player_count',
            field=models.IntegerField(default=8),
        ),
    ]
