from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Category
from .serializers import CategoriesSerializer


# Create your views here.
class CategoriesView(
    generics.ListAPIView
):
    def get_queryset(self):
        return Category.objects.filter(parent_id=None)

    permission_classes = (IsAuthenticated,)
    serializer_class = CategoriesSerializer
