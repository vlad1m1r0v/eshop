from django.contrib import admin
from .models import Payment


# Register your models here.
@admin.register(Payment)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'order', 'created_at', 'status',)
