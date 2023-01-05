from os.path import splitext
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from tinymce import models as tinymce_models
from storages.backends.s3boto3 import S3Boto3Storage
from os.path import splitext


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    file_overwrite = False


def upload_image_to(instance, filename):
    import uuid
    basename, extension = splitext(filename)
    return f'{uuid.uuid4().hex}{extension}'


class FanPage(models.Model):
    class Type(models.TextChoices):
        FACEBOOK = 'facebook'
    page_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    access_token_page = models.CharField(max_length=12288, null=True, blank=True)
    refresh_token_page = models.CharField(max_length=12288, null=True, blank=True)
    avatar_url = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(null=True, default=False)
    app_secret_key = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_subscribe = models.DateTimeField(null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=30, default=Type.FACEBOOK,
        choices=Type.choices)
    fanpage_user_id = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(null=True)
    page_url = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

class UserApp(models.Model):
    external_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.URLField(max_length=10000,null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)

class User(AbstractUser):
    class GenderChoice(models.TextChoices):
        MALE = 'Male'
        FEMALE = 'Female'
        OTHER = 'Other'

    class UserTypeChoice(models.TextChoices):
        CUSTOMER = 'Customer'
        STAFF = 'Staff'
        MANAGER = 'Manager'
        ADMIN = 'Admin'

    gender = models.CharField(max_length=8, null=True, blank=True, choices=GenderChoice.choices)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=upload_image_to)
    country = models.CharField(max_length=255, null=True, blank=True)
    user_type = models.CharField(max_length=255, null=True, blank=True, choices=UserTypeChoice.choices, default=UserTypeChoice.CUSTOMER)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Hotel(models.Model):
    class Rate(models.IntegerChoices):
        ONE = 1,'One'
        TWO = 2,'Two'
        THREE = 3,'Three'
        FOUR = 4,'Four'
        FIVE = 5,'Five'

    name = models.CharField(max_length=100, validators=[MinLengthValidator(8)], null=True, unique=False)
    description = tinymce_models.HTMLField()
    offer = models.IntegerField(null=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    rate_hotel = models.IntegerField(null=True, blank=True, choices=Rate.choices, default=Rate.THREE)
    image = models.ImageField(blank=True, null=True, upload_to=upload_image_to)

    class Meta:
        db_table = 'hotel'


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='hotel_image',
        blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(blank=True, null=True, upload_to=upload_image_to)

    class Meta:
        db_table = 'image_hotel'


class HotelRoom(models.Model):
    class Rate(models.IntegerChoices):
        ONE = 1,'One'
        TWO = 2,'Two'
        THREE = 3,'Three'
        FOUR = 4,'Four'
        FIVE = 5,'Five'

    hotel_id = models.ForeignKey(Hotel, related_name='hotel_room', null=True, blank=True, on_delete=models.SET_NULL)
    room_code = name = models.CharField(max_length=5, validators=[MinLengthValidator(3)], null=True, unique=False)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(8)], null=True, unique=False)
    description = tinymce_models.HTMLField()
    offer = models.IntegerField(null=True)
    rate_hotel_room = models.IntegerField(blank=True, choices=Rate.choices, default=Rate.THREE)
    price = models.FloatField(null=False, blank=False)
    image = models.ImageField(blank=True, null=True, upload_to=upload_image_to)

    class Meta:
        db_table = 'hotel_room'


class RoomImage(models.Model):
    hotel_room = models.ForeignKey(HotelRoom, related_name='hotel_room_image',
        blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(blank=True, null=True, upload_to=upload_image_to)

    class Meta:
        db_table = 'image_room'


class Product(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=False, blank=True)
    detail = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to=upload_image_to)

    class Meta:
        db_table = 'product'


class Bill(models.Model):

    class CustomerTypeChoice(models.TextChoices):
        SIGNED = 'signed'
        GUEST = 'guest'

    room_id = models.ForeignKey(HotelRoom, related_name='room_bill', null=True , blank=True, on_delete=models.SET_NULL)
    customer = models.CharField(max_length=25, blank=True, choices=CustomerTypeChoice.choices, default=CustomerTypeChoice.GUEST)
    refund_money = models.FloatField(blank=True, default=0)
    receive_money = models.FloatField(blank=True, default=0)
    payment = models.FloatField(null=False, blank=True)
    from_date = models.DateTimeField(null=True , blank=True)
    to_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bill'


class BillDetail(models.Model):
    bill_id = models.ForeignKey(HotelRoom, related_name='bill', null=True , blank=True, on_delete=models.SET_NULL)
    product_id = models.ForeignKey(Product, related_name='product', null=True , blank=True, on_delete=models.SET_NULL)
    amount = models.IntegerField(blank=True, default=1)
    price = models.FloatField(null=True, blank=True)
    offer = models.IntegerField(null=True)

    class Meta:
        db_table = 'bill_detail'


class Room(models.Model):
    class TypeRoomChoice(models.TextChoices):
        FACEBOOK = 'facebook'
        ZALO = 'zalo'
        LIVE_CHAT= 'livechat'

    class ApproachCustomerChoice(models.TextChoices):
        FACEBOOK = 'facebook'
        ZALO = 'zalo'
        GOOGLE = 'google'
    class Status(models.TextChoices):
        ALL='all'
        PROCESSING='processing'
        COMPLETED = 'completed'
        EXPIRED ="expired"
    class State(models.TextChoices):
        UNREAD='unread'
        NOT_ANSWER='not_answer'
        REMIND='remind'

    page_id = models.ForeignKey(FanPage, related_name='fanPage_room', null=True, blank=True,
                                on_delete=models.SET_NULL)
    external_id = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=30, default=TypeRoomChoice.FACEBOOK,
                            choices=TypeRoomChoice.choices)
    completed_date = models.DateTimeField(null=True, blank=True)
    conversation_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    room_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=30, default=Status.PROCESSING,
                            choices=Status.choices)
    admin_room_id = models.CharField(max_length=255, null=True, blank=True)
    block_admin = models.BooleanField(null=True)
    last_message_date = models.DateTimeField(auto_now_add=True)
    browser_origin = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        message = Message.objects.filter(room_id = self,log_message_id__isnull=True).order_by('-created_at').first()
        if message:
            self.last_message_date = message.created_at
        super(Room, self).save(*args, **kwargs)


class Message(models.Model):
    class ReactionChoice(models.TextChoices):
        LIKE = 'like'
        LOVE = 'love'
        WOW = 'wow'
        SAD = 'sad'
        ANGRY = 'angry'
        YAY = 'yay'

    uuid = models.CharField(max_length=255, null=True, blank=True)
    room_id = models.ForeignKey(Room, related_name='room_message', null=True, blank=True,
                                on_delete=models.SET_NULL)
    fb_message_id = models.CharField(max_length=255, null=True, blank=True)
    sender_id = models.CharField(max_length=255, null=True, blank=True)
    recipient_id = models.CharField(max_length=255, null=True, blank=True)
    reaction = models.CharField(max_length=30, choices=ReactionChoice.choices, null=True)
    is_forward = models.BooleanField(null=True, default=False)
    reply_id = models.IntegerField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    sender_name = models.CharField(max_length=255, null=True, blank=True)
    is_seen = models.DateTimeField(null=True, blank=True)
    is_sender = models.BooleanField(null=True, default=False)
    remove_for_you = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.FloatField(null=True,blank=True)

    def save(self, *args, **kwargs):
        room = self.room_id
        message = Message.objects.filter(room_id = room,log_message_id__isnull=True).order_by('-created_at').first()
        if message:
            room.last_message_date = message.created_at
            room.save()
        super(Message, self).save(*args, **kwargs)
