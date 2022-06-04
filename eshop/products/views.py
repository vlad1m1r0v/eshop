from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.db.models import OuterRef, Subquery, Prefetch, Case, When, Value, BooleanField, Q

from .filters import ProductFilter
from .models import Product, ProductGallery
from .serializers import ProductsSerializer, ProductSerializer


# Create your views here.
class ProductsView(
    generics.ListAPIView
):
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        # select only first matching image
        subquery = Subquery(
            ProductGallery.objects.filter(product_id=OuterRef('product_id')).values_list('id', flat=True)[0:1])

        return Product.objects.prefetch_related(
            Prefetch('gallery', queryset=ProductGallery.objects.filter(id__in=subquery))
        ).annotate(is_available=Case(When(Q(inventory__amount__gt=0), then=Value(True)), default=Value(False),
                                     output_field=BooleanField())).all()

    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_class = ProductFilter
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductsSerializer
    ordering_fields = ['price', 'created_at']


class ProductView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        product_id = self.kwargs.get('product_id')

        return get_object_or_404(Product.objects.annotate(
            is_available=Case(When(Q(inventory__amount__gt=0), then=Value(True)), default=Value(False),
                              output_field=BooleanField())), id=product_id)
