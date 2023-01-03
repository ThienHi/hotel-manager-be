# Generated by Django 4.0.8 on 2023-01-03 04:04

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import hotel_manager.users.models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('facebook', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True, validators=[django.core.validators.MinLengthValidator(8)])),
                ('description', tinymce.models.HTMLField()),
                ('offer', models.IntegerField(null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('rate_hotel', models.IntegerField(blank=True, choices=[(1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five')], default=3, null=True)),
            ],
            options={
                'db_table': 'hotel',
            },
        ),
        migrations.CreateModel(
            name='HotelRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_code', models.CharField(max_length=5, null=True, validators=[django.core.validators.MinLengthValidator(3)])),
                ('name', models.CharField(max_length=100, null=True, validators=[django.core.validators.MinLengthValidator(8)])),
                ('description', tinymce.models.HTMLField()),
                ('offer', models.IntegerField(null=True)),
                ('rate_hotel_room', models.IntegerField(blank=True, choices=[(1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five')], default=3)),
                ('price', models.FloatField()),
                ('hotel_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hotel_room', to='users.hotel')),
            ],
            options={
                'db_table': 'hotel_room',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('price', models.FloatField(blank=True)),
                ('detail', models.CharField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=hotel_manager.users.models.upload_image_to)),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='RoomImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=hotel_manager.users.models.upload_image_to)),
                ('hotel_room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hotel_room_image', to='users.hotelroom')),
            ],
            options={
                'db_table': 'image_room',
            },
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
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, max_length=255, null=True)),
                ('fb_message_id', models.CharField(blank=True, max_length=255, null=True)),
                ('sender_id', models.CharField(blank=True, max_length=255, null=True)),
                ('recipient_id', models.CharField(blank=True, max_length=255, null=True)),
                ('reaction', models.CharField(choices=[('like', 'Like'), ('love', 'Love'), ('wow', 'Wow'), ('sad', 'Sad'), ('angry', 'Angry'), ('yay', 'Yay')], max_length=30, null=True)),
                ('is_forward', models.BooleanField(default=False, null=True)),
                ('reply_id', models.IntegerField(blank=True, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('sender_name', models.CharField(blank=True, max_length=255, null=True)),
                ('is_seen', models.DateTimeField(blank=True, null=True)),
                ('is_sender', models.BooleanField(default=False, null=True)),
                ('remove_for_you', models.BooleanField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('timestamp', models.FloatField(blank=True, null=True)),
                ('room_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_message', to='users.room')),
            ],
        ),
        migrations.CreateModel(
            name='HotelImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=hotel_manager.users.models.upload_image_to)),
                ('hotel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hotel_image', to='users.hotel')),
            ],
            options={
                'db_table': 'image_hotel',
            },
        ),
        migrations.CreateModel(
            name='BillDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, default=1)),
                ('price', models.FloatField(blank=True, null=True)),
                ('offer', models.IntegerField(null=True)),
                ('bill_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bill', to='users.hotelroom')),
                ('product_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='users.product')),
            ],
            options={
                'db_table': 'bill_detail',
            },
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(blank=True, choices=[('signed', 'Signed'), ('guest', 'Guest')], default='guest', max_length=25)),
                ('refund_money', models.FloatField(blank=True, default=0)),
                ('receive_money', models.FloatField(blank=True, default=0)),
                ('payment', models.FloatField(blank=True)),
                ('from_date', models.DateTimeField(blank=True, null=True)),
                ('to_date', models.DateTimeField(auto_now_add=True)),
                ('room_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_bill', to='users.hotelroom')),
            ],
            options={
                'db_table': 'bill',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=8, null=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('date_of_birth', models.DateTimeField(blank=True, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=hotel_manager.users.models.upload_image_to)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('user_type', models.CharField(blank=True, choices=[('Customer', 'Customer'), ('Staff', 'Staff'), ('Manager', 'Manager'), ('Admin', 'Admin')], default='Customer', max_length=255, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
