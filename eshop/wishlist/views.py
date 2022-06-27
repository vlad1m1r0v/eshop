from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import WishListSerializer, WishListItemSerializer
from .models import WishList, WishListItem
from products.models import Product


# Create your views here.


class WishListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            wish_list_query = WishList.objects.get(user_profile__user=self.request.user)
            wish_list = WishListSerializer(wish_list_query)
            return Response(data=wish_list.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(data={'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        try:
            wish_list_query = WishList.objects.get(user_profile__user=self.request.user)
            product_query = Product.objects.get(pk=request.data['product_id'])
            WishListItem.objects.get_or_create(wish_list=wish_list_query, product=product_query)
            new_wish_list_query = WishList.objects.get(user_profile__user=self.request.user)
            wish_list = WishListSerializer(new_wish_list_query)
            return Response(data=wish_list.data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response(data={'detail': 'List or product with given id not found.'},
                            status=status.HTTP_404_NOT_FOUND)


class RetrieveDestroyWishListView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WishListItemSerializer

    def get_object(self):
        wish_list_query = WishList.objects.get(user_profile__user=self.request.user)
        return get_object_or_404(WishListItem, wish_list=wish_list_query, product_id=self.kwargs.get('product_id'))
