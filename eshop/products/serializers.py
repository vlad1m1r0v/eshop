from rest_framework import serializers
from .models import Product, ProductInventory, ProductDiscount, ProductGallery
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


class ProductGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGallery
        fields = ('image',)


class ProductSerializer(serializers.ModelSerializer):
    inventory = ProductInventorySerializer()
    category = CategoriesBriefSerializer()
    discount = ProductDiscountSerializer()
    gallery = ProductGallerySerializer(many=True)
    is_available = serializers.BooleanField()

    class Meta:
        model = Product
        fields = (
            'pk', 'name', 'SKU', 'category', 'description', 'price', 'characteristics', 'inventory', 'discount',
            'gallery', 'is_available',)

    # flatten nested inventory amount, category name and discount percent
    def to_representation(self, obj):
        representation = super().to_representation(obj)
        flatten_representation = flatten(d=representation, exclude=('characteristics', 'discount',))

        return flatten_representation


class ProductsSerializer(serializers.ModelSerializer):
    category = CategoriesBriefSerializer()
    discount = ProductDiscountSerializer()
    gallery = ProductGallerySerializer(many=True)
    is_available = serializers.BooleanField()

    class Meta:
        model = Product
        fields = ('pk', 'name', 'category', 'description', 'price', 'discount', 'gallery', 'is_available',)

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        # pop from list and assign an object for its further flattening
        list_gallery = representation.pop('gallery')
        image_object = list_gallery[0]
        representation['gallery'] = image_object

        flatten_representation = flatten(d=representation, exclude=('characteristics', 'discount',))
        return flatten_representation
