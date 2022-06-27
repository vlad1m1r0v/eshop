from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from flat_json_widget.widgets import FlatJsonWidget
from .models import Product, ProductGallery, ProductInventory, ProductDiscount


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'SKU', 'category', 'description', 'price', 'created_at')

    formfield_overrides = {
        models.JSONField: {'widget': FlatJsonWidget},
    }


@admin.register(ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} />')

    get_image.short_description = "image"


@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'amount')


@admin.register(ProductDiscount)
class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = ('product', 'description', 'percent', 'active')
