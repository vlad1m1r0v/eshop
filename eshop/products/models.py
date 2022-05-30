from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models import JSONField
from django.core.validators import MinValueValidator, MaxValueValidator
from categories.models import Category
from common.utils.images import crop_and_resize
from common.utils.storage import OverwriteStorage


def gallery_image_path(instance, _):
    count = ProductGallery.objects.filter(product=instance.product).count()
    return 'images/products/{0}/{1}'.format(
        instance.product.name,
        '{}_{}{}'.format(settings.PRODUCT_FILENAME, count + 1, settings.FILENAME_EXTENSION)
    )


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=30, unique=True)
    SKU = models.CharField(max_length=10, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    characteristics = JSONField()

    def __str__(self):
        return f'{self.name}'


class ProductInventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    amount = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Inventories'

    def __str__(self):
        return f'{self.product} {self.amount}'


class ProductDiscount(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='discount')
    description = models.CharField(max_length=100)
    percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Discounts'

    def __str__(self):
        return f'for {self.product} {self.percent}%'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to=gallery_image_path, storage=OverwriteStorage(), blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Gallery'

    def __str__(self):
        return f'{self.product} {self.pk}'

    def save(self, *args, **kwargs):
        image = self.image
        size = {'length': settings.PRODUCT_LENGTH, 'width': settings.PRODUCT_WIDTH}
        cropped_image_file = crop_and_resize(image=image, size=size)
        self.image = cropped_image_file
        super().save(*args, **kwargs)

