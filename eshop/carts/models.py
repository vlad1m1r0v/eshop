import pgtrigger
from django.db import models
from products.models import Product
from users.models import UserProfile


class Cart(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart_owner')

    def __str__(self):
        return f'{self.user_profile}'


@pgtrigger.register(
    # sync with product inventory
    pgtrigger.Trigger(
        name='sync_with_inventory',
        when=pgtrigger.Before,
        operation=pgtrigger.Insert | pgtrigger.Update | pgtrigger.Delete,
        func='UPDATE products_productinventory '
             'SET amount = amount - COALESCE(NEW.amount, 0) + COALESCE(OLD.amount, 0) '
             'WHERE products_productinventory.product_id = COALESCE(NEW.product_id, OLD.product_id); RETURN NEW;',
    )
)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product}'
