from django.contrib import admin
from .models import Order, OrderItem


# Register your models here.
@admin.register(Order)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'status', 'created_at', 'items_amount', 'total_price', )
    readonly_fields = ('items_amount', 'total_price', )


@admin.register(OrderItem)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'amount')
