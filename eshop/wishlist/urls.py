from django.urls import path

from .views import WishListView, RetrieveDestroyWishListView

urlpatterns = [
    path('', WishListView.as_view(), name='wish_list'),
    path('<product_id>', RetrieveDestroyWishListView.as_view(), name='wish_list_item'),
]
