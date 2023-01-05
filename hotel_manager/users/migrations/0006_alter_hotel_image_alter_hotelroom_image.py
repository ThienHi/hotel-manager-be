# Generated by Django 4.0.8 on 2023-01-05 01:54

from django.db import migrations, models
import hotel_manager.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_hotelroom_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=hotel_manager.users.models.upload_image_to),
        ),
        migrations.AlterField(
            model_name='hotelroom',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=hotel_manager.users.models.upload_image_to),
        ),
    ]
