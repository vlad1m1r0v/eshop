from django.urls import path

from .views import ListCreateOrderView

urlpatterns = [
    path('', ListCreateOrderView.as_view(), name='orders'),
]
