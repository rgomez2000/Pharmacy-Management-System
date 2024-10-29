# Generated by Django 5.1.1 on 2024-10-22 01:00

import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("prescriptions", "0005_prescription_created_by"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="prescription",
            name="created_by",
            field=django_currentuser.db.models.fields.CurrentUserField(
                default=django_currentuser.middleware.get_current_authenticated_user,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
