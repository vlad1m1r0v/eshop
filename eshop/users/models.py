from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


def user_avatar_path(instance, _):
    return 'images/avatars/user_{0}/{1}'.format(
        instance.user.profile.pk,
        settings.AVATAR_FILENAME + settings.FILENAME_EXTENSION
    )


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
    )
    birth_date = models.DateTimeField(null=True)
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
        upload_to=user_avatar_path, blank=True, null=True)

    def __str__(self):
        return f'{self.user}'


class UserAddress(models.Model):
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='addresses',
    )
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    zip_code = models.IntegerField()

    def __str__(self):
        return f'{self.user_profile} | {self.country} {self.region} {self.city} {self.region} {self.street} {self.zip_code}'
