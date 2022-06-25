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
        name='sync_with_inventory_after_insert_and_update',
        when=pgtrigger.After,
        operation=pgtrigger.Insert | pgtrigger.Update,
        func='UPDATE products_productinventory '
             'SET amount = amount - COALESCE(NEW.amount, 0) + COALESCE(OLD.amount, 0) '
             'WHERE products_productinventory.product_id = NEW.product_id; RETURN NEW;',
    ),
    pgtrigger.Trigger(
        name='sync_with_inventory_after_delete',
        when=pgtrigger.After,
        operation=pgtrigger.Delete,
        func='UPDATE products_productinventory '
             'SET amount = amount + OLD.amount '
             'WHERE products_productinventory.product_id = OLD.product_id; RETURN NEW;',
    )
)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product}'
