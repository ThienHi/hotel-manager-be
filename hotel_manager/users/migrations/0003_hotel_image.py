# Generated by Django 4.0.8 on 2023-01-04 13:47

from django.db import migrations, models
import hotel_manager.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_hotelroom_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=hotel_manager.users.models.upload_image_to),
        ),
    ]