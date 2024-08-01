from django.urls import path
from .views import VoiceHelpAPIView, VoiceResponseAPIView, ProcessResponseAPIView,  ReceiveProductSelectionAPIView, ReceiveQuantityAPIView, ReceiveMobileNumberAPIView

urlpatterns = [
    path('voice-help/', VoiceHelpAPIView.as_view(), name='voice_help'),
    path('voice-response/', VoiceResponseAPIView.as_view(), name='voice_response'),
    path('process-response/', ProcessResponseAPIView.as_view(), name='process_response'),
    path('receive-product-selection/', ReceiveProductSelectionAPIView.as_view(), name='receive_product_selection'),
    path('receive-quantity/', ReceiveQuantityAPIView.as_view(), name='receive_quantity'),
    path('receive-mobile-number/', ReceiveMobileNumberAPIView.as_view(), name = 'receive-mobile')
]