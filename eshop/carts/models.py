import pgtrigger
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from products.models import Product, ProductDiscount
from users.models import UserProfile


class Cart(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart_owner')

    @property
    def items_amount(self):
        return CartItem.objects.filter(cart=self.pk).count()

    @property
    def total_price(self):
        price = 0
        cart_items = CartItem.objects.filter(cart=self.pk)
        for item in cart_items:
            try:
                item_discount = ProductDiscount.objects.get(product=item.product, active=True).percent
                price += item.amount * item.product.price * (1 - item_discount / 100)
            except ObjectDoesNotExist:
                price += item.amount * item.product.price

        return price

    def __str__(self):
        return f'{self.user_profile}'


@pgtrigger.register(
    # sync with product inventory
    pgtrigger.Trigger(
        name='sync_cart_with_inventory',
        when=pgtrigger.Before,
        operation=pgtrigger.Insert | pgtrigger.Update | pgtrigger.Delete,
        func='UPDATE products_productinventory '
             'SET amount = amount - COALESCE(NEW.amount, 0) + COALESCE(OLD.amount, 0) '
             'WHERE products_productinventory.product_id = COALESCE(NEW.product_id, OLD.product_id); RETURN NEW;',
    )
)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product}'
