from django.contrib import admin
from .models import Cart, CartItem


# Register your models here.
@admin.register(Cart)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile',)


@admin.register(CartItem)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'amount')
