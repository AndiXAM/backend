# Generated by Django 5.1.3 on 2024-11-18 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testpril', '0002_tournament_date_tournament_player_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='players',
            field=models.ManyToManyField(related_name='teams', to='testpril.player'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
