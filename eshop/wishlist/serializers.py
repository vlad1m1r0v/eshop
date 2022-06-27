from rest_framework import serializers
from products.serializers import ProductsSerializer
from .models import WishList, WishListItem


class WishListItemSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()
    created_at = serializers.DateTimeField()

    class Meta:
        model = WishListItem
        fields = ('product', 'created_at')


class WishListSerializer(serializers.ModelSerializer):
    items = WishListItemSerializer(many=True)

    class Meta:
        model = WishList
        fields = ('items',)
