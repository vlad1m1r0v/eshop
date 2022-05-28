from django.urls import path
from .views import ProductsView, ProductView

urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    path('<product_id>', ProductView.as_view(), name='product'),
]
