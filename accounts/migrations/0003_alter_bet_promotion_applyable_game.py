# Generated by Django 4.1.2 on 2022-11-30 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_alter_game_game_id'),
        ('accounts', '0002_promotion_deposit_promotion_bet_promotion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet_promotion',
            name='applyable_game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.game', unique=True),
        ),
    ]
