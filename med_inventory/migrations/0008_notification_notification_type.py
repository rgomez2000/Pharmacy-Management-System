# Generated by Django 5.1.1 on 2024-11-12 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med_inventory', '0007_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
