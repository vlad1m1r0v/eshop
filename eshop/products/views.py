from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .filters import ProductFilter
from .models import Product
from .serializers import ProductsSerializer, ProductSerializer


# Create your views here.
class ProductsView(
    generics.ListAPIView
):
    def get_queryset(self):
        return Product.objects.all()

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

        return get_object_or_404(Product, id=product_id)
