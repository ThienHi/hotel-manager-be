# Generated by Django 4.0.8 on 2023-01-02 15:38

from django.db import migrations, models
import django.db.models.deletion
import hotel_manager.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0001_initial'),
        ('users', '0003_alter_hotel_rate_hotel_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='fb_message_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='is_forward',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='is_seen',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='reaction',
            field=models.CharField(choices=[('like', 'Like'), ('love', 'Love'), ('wow', 'Wow'), ('sad', 'Sad'), ('angry', 'Angry'), ('yay', 'Yay')], max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='remove_for_you',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='reply_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='sender_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=hotel_manager.users.models.upload_image_to),
        ),
        migrations.AlterModelTable(
            name='message',
            table=None,
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=255, null=True)),
                ('user_id', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('approved_date', models.DateTimeField(blank=True, null=True)),
                ('type', models.CharField(choices=[('facebook', 'Facebook'), ('zalo', 'Zalo'), ('livechat', 'Live Chat')], default='facebook', max_length=30)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('conversation_id', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('room_id', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('all', 'All'), ('processing', 'Processing'), ('completed', 'Completed'), ('expired', 'Expired')], default='processing', max_length=30)),
                ('admin_room_id', models.CharField(blank=True, max_length=255, null=True)),
                ('block_admin', models.BooleanField(null=True)),
                ('last_message_date', models.DateTimeField(auto_now_add=True)),
                ('browser_origin', models.CharField(blank=True, max_length=500, null=True)),
                ('page_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fanPage_room', to='facebook.fanpage')),
            ],
        ),
        migrations.AlterField(
            model_name='message',
            name='room_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_message', to='users.room'),
        ),
        migrations.DeleteModel(
            name='RoomMessage',
        ),
    ]