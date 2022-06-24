from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import WishListSerializer
from .models import WishList, WishListItem


# Create your views here.


class WishListView(APIView):
    serializer_class = WishListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            query_obj = WishList.objects.get(user_profile__user=self.request.user)
            wish_list = WishListSerializer(query_obj)
            return Response(data=wish_list.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(data={'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
