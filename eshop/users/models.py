from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


def user_avatar_path(instance, _):
    return 'images/avatars/user_{0}/{1}'.format(
        instance.user.profile.uu_id,
        settings.AVATAR_FILENAME + settings.AVATAR_FILENAME_EXTENSION
    )


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
    )
    birth_date = models.DateTimeField()
    MALE = 'Male'
    FEMALE = 'Female'
    ANOTHER = 'Another'
    GENDER_CHOICES = [
        MALE,
        FEMALE,
        ANOTHER
    ]
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES, default=ANOTHER)
    phone_number = PhoneNumberField(region='UA')
    avatar = models.ImageField(blank=True, null=True, upload_to=user_avatar_path)


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

