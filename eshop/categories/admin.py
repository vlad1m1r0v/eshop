from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category


# Register your models here.

@admin.register(Category)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'parent',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} />')

    get_image.short_description = "image"
