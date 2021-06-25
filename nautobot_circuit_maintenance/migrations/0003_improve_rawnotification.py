# Generated by Django 3.1.10 on 2021-06-10 09:15

from django.db import migrations, models
import django.db.models.deletion


def migrate_source(apps, schema_editor):
    """Migrate from old text Source to new reference to Notification Source."""

    RawNotificationModel = apps.get_model("nautobot_circuit_maintenance", "RawNotification")
    NotificationSourceModel = apps.get_model("nautobot_circuit_maintenance", "NotificationSource")

    for raw_notification in RawNotificationModel.objects.all():
        raw_notification.source = NotificationSourceModel.objects.get(name=raw_notification.source_old)
        raw_notification.save()


class Migration(migrations.Migration):

    dependencies = [
        ("nautobot_circuit_maintenance", "0002_notification_secrets_out_of_db"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rawnotification",
            name="sender",
            field=models.CharField(blank=True, default="", max_length=200, null=True),
        ),
        migrations.RenameField(
            model_name="rawnotification",
            old_name="source",
            new_name="source_old",
        ),
        migrations.AddField(
            model_name="rawnotification",
            name="source",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="nautobot_circuit_maintenance.notificationsource",
            ),
        ),
        migrations.RunPython(migrate_source),
        migrations.RemoveField(
            model_name="rawnotification",
            name="source_old",
        ),
    ]
