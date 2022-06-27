from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from common.utils.images import crop_and_resize
from common.utils.storage import OverwriteStorage


def user_avatar_path(instance, _):
    return 'images/avatars/{0}/{1}'.format(
        instance.user.username,
        settings.AVATAR_FILENAME + settings.FILENAME_EXTENSION
    )


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
    )
    birth_date = models.DateField(null=True)
    MALE = 'Male'
    FEMALE = 'Female'
    ANOTHER = 'Another'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (ANOTHER, 'Another')
    ]
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES, default=ANOTHER)
    phone_number = PhoneNumberField(region='UA', null=True)
    avatar = models.ImageField(
        upload_to=user_avatar_path, storage=OverwriteStorage(), blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Profiles'

    def save(self, *args, **kwargs):
        if self.avatar:
            image = self.avatar
            size = {'length': settings.AVATAR_SIZE, 'width': settings.AVATAR_SIZE}
            cropped_image_file = crop_and_resize(image=image, size=size)
            self.avatar = cropped_image_file
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user}'


class UserAddress(models.Model):
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='addresses',
    )
    country = models.CharField(max_length=30)
    region = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    zip_code = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'{self.country} {self.city} {self.zip_code}'
