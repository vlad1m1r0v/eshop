from rest_framework import serializers
from .models import Product, ProductInventory, ProductDiscount
from categories.serializers import CategoriesBriefSerializer
from common.utils.dict import flatten


class ProductInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventory
        fields = ('amount',)


class ProductDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDiscount
        fields = ('description', 'percent', 'active')


class ProductSerializer(serializers.ModelSerializer):
    inventory = ProductInventorySerializer()
    category = CategoriesBriefSerializer()
    discount = ProductDiscountSerializer()

    class Meta:
        model = Product
        fields = ('pk', 'name', 'SKU', 'category', 'description', 'price', 'characteristics', 'inventory', 'discount',)

    # flatten nested inventory amount, category name and discount percent
    def to_representation(self, obj):
        representation = super().to_representation(obj)
        flatten_representation = flatten(d=representation, exclude=('characteristics', 'discount'))
        return flatten_representation


class ProductsSerializer(serializers.ModelSerializer):
    category = CategoriesBriefSerializer()
    discount = ProductDiscountSerializer()

    class Meta:
        model = Product
        fields = ('pk', 'name', 'category', 'description', 'price', 'discount',)

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        flatten_representation = flatten(d=representation, exclude=('characteristics', 'discount'))
        return flatten_representation
