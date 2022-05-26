from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import UserProfile, UserAddress


# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'gender', 'phone_number',)
    readonly_fields = ('get_avatar',)

    def get_avatar(self, obj):
        return mark_safe(f'<img src={obj.avatar.url} />')

    get_avatar.short_description = "avatar"


@admin.register(UserAddress)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'country', 'region', 'city', 'street', 'zip_code')

