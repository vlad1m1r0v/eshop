from django.urls import path
from .views import CurrentUserView

urlpatterns = [
    path('current-user', CurrentUserView.as_view(), name='users_current_user'),
]
