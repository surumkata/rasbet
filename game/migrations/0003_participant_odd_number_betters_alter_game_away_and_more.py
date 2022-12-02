# Generated by Django 4.1.2 on 2022-12-02 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_alter_game_game_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('is_team', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='odd',
            name='number_betters',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='away',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away', to='game.participant'),
        ),
        migrations.AlterField(
            model_name='game',
            name='home',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home', to='game.participant'),
        ),
    ]
