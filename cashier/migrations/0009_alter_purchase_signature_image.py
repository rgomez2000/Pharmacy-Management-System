# Generated by Django 5.1.3 on 2024-11-24 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0008_alter_purchase_signature_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='signature_image',
            field=models.ImageField(null=True, upload_to='signatures/'),
        ),
    ]
