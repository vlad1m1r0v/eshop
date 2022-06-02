import django_filters
from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Product


class ProductFilter(filters.FilterSet):
    price = filters.RangeFilter()
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')
    category = django_filters.CharFilter(method='category_filter', label="category")

    class Meta:
        model = Product
        fields = ['category', 'price', 'name']

    def category_filter(self, queryset, name, value):
        values = value.split(',')
        return queryset.filter(
            Q(category__name__in=values) | Q(category__parent__name__in=values))
