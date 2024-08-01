from django.urls import path
from .views import StripeCheckoutView, StripeWebhookView

urlpatterns = [
    path('Checkout/', StripeCheckoutView.as_view(), name='stripe_checkout'),
    # path('status/', StripeCheckoutView.as_view(), name = 'status'),
    path('webhook/', StripeWebhookView.as_view(), name='stripe_webhook')
]