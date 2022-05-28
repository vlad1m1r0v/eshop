from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .models import Product
from .serializers import ProductsSerializer, ProductSerializer


# Create your views here.
class ProductsView(
    generics.ListAPIView
):
    def get_queryset(self):
        return Product.objects.all()

    permission_classes = (IsAuthenticated,)
    serializer_class = ProductsSerializer


class ProductView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(
            Product,
            id=self.kwargs.get('product_id'))
