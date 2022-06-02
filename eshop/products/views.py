from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.db.models import OuterRef, Subquery, Prefetch

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
        ).all()

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductsSerializer



class ProductView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        product_id = self.kwargs.get('product_id')

        return get_object_or_404(Product, id=product_id)
