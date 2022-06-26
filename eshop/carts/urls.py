from django.urls import path

from .views import CartView, RetrieveDestroyWishListView, IncrementView, DecrementView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('<product_id>', RetrieveDestroyWishListView.as_view(), name='cart_item'),
    path('<product_id>/increment', IncrementView.as_view(), name='increment_item'),
    path('<product_id>/decrement', DecrementView.as_view(), name='decrement_item'),

]
