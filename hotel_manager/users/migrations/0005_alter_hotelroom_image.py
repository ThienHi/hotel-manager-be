# Generated by Django 4.0.8 on 2023-01-04 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_hotel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelroom',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
