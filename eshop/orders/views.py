from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from rest_framework import status
from carts.models import CartItem, Cart
from users.models import UserProfile
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderBriefSerializer


class ListCreateOrderView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderBriefSerializer

    def get_queryset(self):
        return Order.objects.filter(user_profile__user=self.request.user)

    def perform_create(self, serializer):
        user_cart = Cart.objects.get(user_profile__user=self.request.user)
        cart_items = CartItem.objects.filter(cart=user_cart)
        user_order_exists = Order.objects.filter(user_profile__user=self.request.user, status='accepted').exists()
        if not user_order_exists:
            user_profile = UserProfile.objects.get(user=self.request.user)
            user_order = Order(user_profile=user_profile)
            user_order.save()
        last_accepted_order = Order.objects.filter(user_profile__user=self.request.user,
                                                   status='accepted').order_by('-created_at').first()
        for item in cart_items:
            order_item = OrderItem(order=last_accepted_order, product=item.product, amount=item.amount)
            item.delete()
            order_item.save()


class RetrieveDestroyOrderView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_object(self):
        return get_object_or_404(
            Order,
            id=self.kwargs.get('order_id'),
            user_profile__user=self.request.user)
