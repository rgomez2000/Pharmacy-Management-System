# Generated by Django 5.1.1 on 2024-11-03 16:14

import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("logs", "0004_remove_prescriptionlog_patient_name_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="prescriptionlog",
            name="pharmacist_name",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
