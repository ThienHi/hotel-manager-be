from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "hotel_manager.facebook"
    verbose_name = _("Facebook")
