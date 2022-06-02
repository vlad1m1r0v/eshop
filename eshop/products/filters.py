import django_filters
from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Product


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = django_filters.CharFilter(method='category_filter', label="category")
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']

    def category_filter(self, queryset, name, value):
        return queryset.filter(
            Q(category__name__iexact=value) | Q(category__parent__name__iexact=value))
