from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import RetrieveDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from .permissions import IncrementPermission, DecrementPermission


# Create your views here.
class CartView(APIView):
    permission_classes = (IsAuthenticated, IncrementPermission,)

    def get(self, request):
        try:
            cart_query = Cart.objects.get(user_profile__user=self.request.user)
            cart = CartSerializer(cart_query)
            return Response(data=cart.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(data={'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        try:
            cart_query = Cart.objects.get(user_profile__user=self.request.user)
            product_query = Product.objects.get(pk=request.data['product_id'])
            CartItem.objects.get_or_create(cart=cart_query, product=product_query)
            new_cart_query = Cart.objects.get(user_profile__user=self.request.user)
            new_cart = CartSerializer(new_cart_query)
            return Response(data=new_cart.data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response(data={'detail': 'Cart or product with given id not found.'},
                            status=status.HTTP_404_NOT_FOUND)


class RetrieveDestroyWishListView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartItemSerializer

    def get_object(self):
        cart_query = Cart.objects.get(user_profile__user=self.request.user)
        return get_object_or_404(CartItem, cart=cart_query, product_id=self.kwargs.get('product_id'))


class IncrementView(APIView):
    permission_classes = (IsAuthenticated, IncrementPermission,)

    def patch(self, *args, **kwargs):
        try:
            cart_query = Cart.objects.get(user_profile__user=self.request.user)
            cart_item_query = CartItem.objects.get(cart=cart_query, product_id=self.kwargs.get('product_id'))
            cart_item_query.amount += 1
            cart_item_query.save()
            cart_item = CartItemSerializer(cart_item_query)
            return Response(data=cart_item.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(data={'detail': 'Cart or product with given id not found.'},
                            status=status.HTTP_404_NOT_FOUND)


class DecrementView(APIView):
    permission_classes = (IsAuthenticated, DecrementPermission,)

    def patch(self, *args, **kwargs):
        try:
            cart_query = Cart.objects.get(user_profile__user=self.request.user)
            cart_item_query = CartItem.objects.get(cart=cart_query, product_id=self.kwargs.get('product_id'))
            cart_item_query.amount -= 1
            cart_item_query.save()
            cart_item = CartItemSerializer(cart_item_query)
            return Response(data=cart_item.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(data={'detail': 'Cart or product with given id not found.'},
                            status=status.HTTP_404_NOT_FOUND)
