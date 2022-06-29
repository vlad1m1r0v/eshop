from rest_framework import serializers
from products.serializers import ProductsSerializer
from .models import Order, OrderItem


class OrderBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('pk', 'status', 'created_at', 'items_amount', 'total_price',)


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()

    class Meta:
        model = OrderItem
        fields = ('product', 'amount',)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('pk', 'status', 'created_at', 'items', 'items_amount', 'total_price',)
