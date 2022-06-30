from django.urls import path

from .views import ListCreateOrderView, RetrieveDestroyOrderView

urlpatterns = [
    path('', ListCreateOrderView.as_view(), name='orders'),
    path('<order_id>', RetrieveDestroyOrderView.as_view(), name='orders_order'),
]
