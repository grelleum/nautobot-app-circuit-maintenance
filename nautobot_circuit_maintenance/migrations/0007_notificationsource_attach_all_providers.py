# Generated by Django 3.1.13 on 2021-08-11 06:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nautobot_circuit_maintenance", "0006_fake_migration_to_update_custom_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="notificationsource",
            name="attach_all_providers",
            field=models.BooleanField(default=False),
        ),
    ]
