# Generated by Django 4.1.2 on 2022-11-02 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0003_alter_game_datetime_alter_odd_happened"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game", name="datetime", field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="game",
            name="game_id",
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
