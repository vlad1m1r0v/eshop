from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import WishListSerializer
from .models import WishList


# Create your views here.


class WishListView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WishListSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(
            WishList,
            user_profile__user=self.request.user)
