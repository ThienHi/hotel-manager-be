# Generated by Django 4.0.8 on 2023-01-04 13:45

from django.db import migrations, models
import hotel_manager.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelroom',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=hotel_manager.users.models.upload_image_to),
        ),
    ]
