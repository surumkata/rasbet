# Generated by Django 4.1.2 on 2022-11-04 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_rename_admin_ad'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ad',
            new_name='Admin',
        ),
    ]