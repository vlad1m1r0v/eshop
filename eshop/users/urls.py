from django.urls import path
from .views import GetCurrentUserView, UpdateCurrentUser

urlpatterns = [
    path('current-user', GetCurrentUserView.as_view(), name='users_current_user'),
    path('update', UpdateCurrentUser.as_view(), name='users_update_current_user'),
]
