from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from products.models import ProductInventory


class IncrementPermission(permissions.BasePermission):
    message = 'no longer available'

    def has_permission(self, request, view):
        product_id = request.data['product_id']
        can_increment = ProductInventory.objects.filter(product_id=product_id, amount__gt=0).exists()
        return can_increment or request.method in SAFE_METHODS
