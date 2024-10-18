# Generated by Django 5.1.1 on 2024-10-18 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_userprofile_password_changed"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="password_changed",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="password_requires_change",
            field=models.BooleanField(default=True),
        ),
    ]
