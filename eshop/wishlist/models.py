from django.db import models

from products.models import Product
from users.models import UserProfile


# Create your models here.


class WishList(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f'{self.user_profile}'


class WishListItem(models.Model):
    wish_list = models.ForeignKey(WishList, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product}'
