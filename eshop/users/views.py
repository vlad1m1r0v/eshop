from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from .models import UserProfile


# Create your views here.
class GetCurrentUserView(RetrieveAPIView):
    def get_object(self):
        return UserProfile.objects.filter(user=self.request.user).first()

    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer


class UpdateCurrentUser(UpdateAPIView):
    def get_object(self):
        return UserProfile.objects.filter(user=self.request.user).first()

    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
