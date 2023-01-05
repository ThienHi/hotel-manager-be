# Generated by Django 4.0.8 on 2023-01-05 08:02

from django.db import migrations, models
import django.db.models.deletion
import hotel_manager.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_hotel_image_alter_hotelroom_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to=hotel_manager.users.models.upload_image_to)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.CharField(blank=True, max_length=500, null=True)),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('size', models.IntegerField(blank=True, null=True)),
                ('mid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_id', to='users.message')),
            ],
        ),
    ]