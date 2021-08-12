# Generated by Django 3.1.13 on 2021-08-09 15:16

from django.db import migrations, models


def convert_raw_from_str_to_bytes(apps, schema_editor):
    """Convert raw from str to bytes."""
    RawNotificationModel = apps.get_model("nautobot_circuit_maintenance", "RawNotification")

    for raw_notification in RawNotificationModel.objects.all():
        raw_txt = raw_notification.raw
        # Removing b'' from previous literal conversion from bytes to TextField
        raw_txt = raw_txt.strip("b'").strip("'")
        raw_notification.raw_b = raw_txt.encode()
        raw_notification.save(update_fields=["raw_b"])


class Migration(migrations.Migration):

    dependencies = [
        ("nautobot_circuit_maintenance", "0007_notificationsource_attach_all_providers"),
    ]

    operations = [
        migrations.AddField(
            model_name="rawnotification",
            name="raw_b",
            field=models.BinaryField(null=True),
        ),
        migrations.RunPython(convert_raw_from_str_to_bytes),
        migrations.RemoveField(
            model_name="rawnotification",
            name="raw",
        ),
        migrations.RenameField(
            model_name="rawnotification",
            old_name="raw_b",
            new_name="raw",
        ),
        migrations.AlterField(
            model_name="rawnotification",
            name="raw",
            field=models.BinaryField(),
        ),
    ]