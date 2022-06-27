from django.db.models.signals import post_save
from users.models import UserProfile
from .models import Cart


def create_wish_list(created, instance, **kwargs):
    if created:
        Cart.objects.create(user_profile=instance)


post_save.connect(create_wish_list, sender=UserProfile)
