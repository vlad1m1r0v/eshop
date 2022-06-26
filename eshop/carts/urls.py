from django.urls import path

from .views import CartView, RetrieveDestroyWishListView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('<product_id>', RetrieveDestroyWishListView.as_view(), name='cart item'),
]
