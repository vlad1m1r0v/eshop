from django.contrib import admin
from .models import WishList, WishListItem


# Register your models here.
@admin.register(WishList)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile',)


@admin.register(WishListItem)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('wish_list', 'product', 'created_at')
