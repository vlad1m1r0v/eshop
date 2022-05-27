from django.db import models
from django.conf import settings
from common.utils.images import crop_and_resize
from common.utils.storage import OverwriteStorage


# Create your models here.


def category_image_path(instance, _):
    return 'images/categories/{0}/{1}'.format(
        instance.name,
        settings.CATEGORY_FILENAME + settings.FILENAME_EXTENSION
    )


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='subcategories')
    image = models.ImageField(
        upload_to=category_image_path, storage=OverwriteStorage(), blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        image = self.image
        length = width = settings.CATEGORY_SIZE if self.parent is None else settings.SUBCATEGORY_SIZE
        size = {'length': length, 'width': width}
        cropped_image_file = crop_and_resize(image=image, size=size)
        self.image = cropped_image_file
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'
