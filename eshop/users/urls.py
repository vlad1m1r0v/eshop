from django.urls import path
from .views import CurrentUserView, UserAddressesView, UserAddressView

urlpatterns = [
    path('current-user', CurrentUserView.as_view(), name='users_current_user'),
    path('current-user/address', UserAddressesView.as_view(), name='users_current_user_addresses'),
    path('current-user/address/<user_address_id>', UserAddressView.as_view(), name='users_current_user_address')
]
