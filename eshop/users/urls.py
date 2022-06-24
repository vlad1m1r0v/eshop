from django.urls import path
from wishlist.views import WishListView, RetrieveDestroyWishListView
from .views import CurrentUserView, UserAddressesView, UserAddressView

urlpatterns = [
    path('current-user', CurrentUserView.as_view(), name='users_current_user'),
    path('current-user/addresses', UserAddressesView.as_view(), name='users_current_user_addresses'),
    path('current-user/addresses/<user_address_id>', UserAddressView.as_view(), name='users_current_user_address'),
    path('current-user/wishlist', WishListView.as_view(), name='users_current_wish_list'),
    path('current-user/wishlist/<product_id>', RetrieveDestroyWishListView.as_view(),
         name='users_current_wish_list_item')
]
