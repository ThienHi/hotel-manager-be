from django.contrib import admin
from hotel_manager.users.models import FanPage, UserApp

@admin.register(FanPage)
class FanPageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FanPage._meta.fields if field.name != 'description']

@admin.register(UserApp)
class UserAppAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserApp._meta.fields if field.name != 'description']