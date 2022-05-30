from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.db.models import OuterRef, Subquery, Prefetch
from .models import Product, ProductGallery
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

    # def get_object(self):
    #     product_id = self.kwargs.get('product_id')
    #     subquery = Subquery(ProductGallery.objects.filter(product_id=OuterRef('product_id')))
    #
    #     return Product.objects.prefetch_related(
    #         Prefetch('gallery', queryset=subquery)).filter(id=product_id)

    def get_object(self):
        product_id = self.kwargs.get('product_id')
        # select only first matching image
        subquery = Subquery(
            ProductGallery.objects.filter(product_id=OuterRef('product_id')).values_list('id', flat=True)[0:1])

        return get_object_or_404(
            Product.objects.prefetch_related(
                Prefetch('gallery', queryset=ProductGallery.objects.filter(id__in=subquery))
            ), id=product_id)
