# Generated by Django 4.1.2 on 2022-10-24 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        (
            "accounts",
            "0004_remove_payment_method_id_alter_payment_method_method_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Bet",
            fields=[
                ("betID", models.AutoField(primary_key=True, serialize=False)),
                ("amount", models.FloatField()),
                ("total_odd", models.FloatField()),
                ("datetime", models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Bet_type",
            fields=[
                (
                    "type",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
            ],
        ),
        migrations.CreateModel(
            name="History",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "betID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="gamble.bet"
                    ),
                ),
                (
                    "userID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="accounts.user"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="bet",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="gamble.bet_type"
            ),
        ),
    ]
