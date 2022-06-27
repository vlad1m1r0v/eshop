from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from products.models import ProductInventory
from .models import Cart, CartItem


class IncrementPermission(permissions.BasePermission):
    message = 'no longer available'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        # get product_id from URL or request data
        product_id = request.data.get('product_id') or request.resolver_match.kwargs.get('product_id')
        can_increment = ProductInventory.objects.filter(product_id=product_id, amount__gt=0).exists()
        return can_increment


class DecrementPermission(permissions.BasePermission):
    message = 'amount can\'t be less than 1'

    def has_permission(self, request, view):
        product_id = request.resolver_match.kwargs.get('product_id')
        user_cart = Cart.objects.get(user_profile__user=request.user)
        can_decrement = CartItem.objects.filter(cart=user_cart, product_id=product_id, amount__gt=1).exists()
        return can_decrement
