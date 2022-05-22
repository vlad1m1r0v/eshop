from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer, UserAddressSerializer
from .models import UserProfile, UserAddress
from .utils import crop_and_resize


# Create your views here.
class CurrentUserView(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      generics.GenericAPIView):
    def get_object(self):
        return UserProfile.objects.filter(user=self.request.user).first()

    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def perform_update(self, serializer):
        if 'avatar' in serializer.validated_data:
            image = serializer.validated_data['avatar']
            cropped_image_file = crop_and_resize(image)
            serializer.validated_data['avatar'] = cropped_image_file
        serializer.save()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class UserAddressesView(generics.ListCreateAPIView):
    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserAddress.objects.filter(user_profile__user=self.request.user)

    def perform_create(self, serializer, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(user_profile=profile)


class UserAddressView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(
            UserAddress,
            id=self.kwargs.get('user_address_id'),
            user_profile__user=self.request.user)
