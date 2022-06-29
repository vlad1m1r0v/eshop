import pgtrigger
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

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def items_amount(self):
        return OrderItem.objects.filter(order_id=self.pk).count()

    def __str__(self):
        return f'{self.user_profile}'


@pgtrigger.register(
    # sync with product inventory
    pgtrigger.Trigger(
        name='sync_order_with_inventory',
        when=pgtrigger.After,
        operation=pgtrigger.Insert | pgtrigger.Update | pgtrigger.Delete,
        func='UPDATE products_productinventory '
             'SET amount = amount - COALESCE(NEW.amount, 0) + COALESCE(OLD.amount, 0) '
             'WHERE products_productinventory.product_id = COALESCE(NEW.product_id, OLD.product_id); RETURN NEW;',
    )
)
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
