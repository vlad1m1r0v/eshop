from rest_framework import serializers
from products.serializers import ProductsSerializer
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()

    class Meta:
        model = CartItem
        fields = ('product', 'amount')


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('items',)
