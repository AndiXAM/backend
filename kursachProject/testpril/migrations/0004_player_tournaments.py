# Generated by Django 5.1.3 on 2024-11-18 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testpril', '0003_alter_team_players_alter_tournament_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='tournaments',
            field=models.ManyToManyField(related_name='players', to='testpril.tournament'),
        ),
    ]
