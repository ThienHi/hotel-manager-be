from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from hotel_manager.users.models import Hotel, HotelRoom, Bill, BillDetail, Product, Message, Room
from hotel_manager.users.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "is_superuser"]


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Hotel._meta.fields if field.name != 'description']


@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = [field.name for field in HotelRoom._meta.fields if field.name != 'description']


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Bill._meta.fields if field.name != 'description']


@admin.register(BillDetail)
class BillDetailAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BillDetail._meta.fields if field.name != 'description']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields if field.name != 'description']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Message._meta.fields if field.name != 'description']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Room._meta.fields if field.name != 'description']