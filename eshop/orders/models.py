from django.db import models
from users.models import UserProfile
from products.models import Product
from datetime import datetime


class Order(models.Model):
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='orders',
    )

    ACCEPTED = 'accepted'
    COMPLETED = 'completed'
    REJECTED = 'rejected'
    CANCELLED = 'cancelled'

    status_choices = [
        (ACCEPTED, 'accepted'),
        (COMPLETED, 'completed'),
        (REJECTED, 'rejected'),
        (CANCELLED, 'cancelled')
    ]
    status = models.CharField(
        max_length=20,
        choices=status_choices,
        default=ACCEPTED
    )

    created_at = models.DateTimeField(default=datetime.now())

    @property
    def items_amount(self):
        return OrderItem.objects.filter(order_id=self.pk).count()

    def __str__(self):
        return f'{self.user_profile}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    amount = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.product}'
