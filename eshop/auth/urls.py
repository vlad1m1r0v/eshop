from django.urls import path
from .views import MyObtainTokenPairView, RegisterView, ChangePasswordView, UpdateProfileView, LogoutView, LogoutAllView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterView.as_view(), name='auth_register'),
    path('change-password', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update-profile', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('logout', LogoutView.as_view(), name='auth_logout'),
    path('logout-all', LogoutAllView.as_view(), name='auth_logout_all'),
]

