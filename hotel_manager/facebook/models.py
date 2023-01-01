from django.utils.translation import gettext_lazy as _
from django.db import models


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