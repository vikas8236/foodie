from django.urls import path
from .views import CheckoutAPIView, PaymentConfirmationAPIView

urlpatterns = [
    path('checkout/', CheckoutAPIView.as_view(), name='checkout-products'),
    path('confirm/<int:order_id>/', PaymentConfirmationAPIView.as_view(), name = 'confirm-checkout'),
]