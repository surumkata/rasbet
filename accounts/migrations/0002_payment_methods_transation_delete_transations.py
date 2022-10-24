# Generated by Django 4.1.2 on 2022-10-24 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment_methods",
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
                ("method", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Transation",
            fields=[
                ("transationID", models.AutoField(primary_key=True, serialize=False)),
                ("type", models.CharField(max_length=50)),
                ("amount", models.FloatField()),
                ("datetime", models.DateTimeField()),
                (
                    "method",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.payment_methods",
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
        migrations.DeleteModel(name="Transations",),
    ]
