from django.db import models
from django.conf import settings


# Create your models here.

def category_picture_path(instance, _):
    return 'images/avatars/user_{0}/{1}'.format(
        instance.user.profile.pk,
        settings.CATEGORY_FILENAME + settings.FILENAME_EXTENSION
    )


class Category(models.Model):
    name = models.CharField(min_length=3, max_length=15)
    description = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    picture = models.ImageField(
        upload_to=category_picture_path, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'





