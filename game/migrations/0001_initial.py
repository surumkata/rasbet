# Generated by Django 4.1.2 on 2022-11-28 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('competition', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('country', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('game_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('home', models.CharField(max_length=50)),
                ('away', models.CharField(max_length=50)),
                ('home_score', models.IntegerField(default=0)),
                ('away_score', models.IntegerField(default=0)),
                ('datetime', models.DateTimeField()),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.competition')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.country')),
            ],
        ),
        migrations.CreateModel(
            name='Odd_type',
            fields=[
                ('type', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('sport', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('has_draw', models.BooleanField()),
                ('is_team_sport', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('state', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Odd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('odd', models.FloatField()),
                ('happened', models.BooleanField(default=False)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.game')),
                ('odd_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.odd_type')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.sport'),
        ),
        migrations.AddField(
            model_name='game',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.state'),
        ),
        migrations.AddField(
            model_name='competition',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.country'),
        ),
        migrations.AddField(
            model_name='competition',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.sport'),
        ),
    ]
