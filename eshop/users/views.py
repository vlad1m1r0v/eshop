from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from .models import UserProfile


# Create your views here.
class CurrentUserView(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      generics.GenericAPIView):
    def get_object(self):
        return UserProfile.objects.filter(user=self.request.user).first()

    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
