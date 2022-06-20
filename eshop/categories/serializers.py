from rest_framework import serializers
from common.serializers.recursive_field import RecursiveField
from common.serializers.non_empty import NonEmptySerializer
from .models import Category


class CategoriesSerializer(NonEmptySerializer):
    subcategories = RecursiveField(many=True)

    class Meta:
        model = Category
        fields = ('name', 'description', 'image', 'subcategories')


class CategoriesBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)
