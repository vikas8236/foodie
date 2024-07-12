
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Order
from .serializers import CheckoutSerializer, OrderSerializer
import stripe

stripe.api_key = 'sk_test_51PbgshRohX98q0M7Kjnp5WHQdFqYTyvRHoYpbaHPDisqHkxTUIFq8g9J2B7c8x2Z7ROdJzmFi4Qjlw8JSJueKwDX00Y8MiJtnb'

class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            order_serializer = OrderSerializer(order)
            return Response({
                'order': order_serializer.data,
                'client_secret': order.stripe_payment_intent
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentConfirmationAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = Order.objects.get(id=order_id)
        payment_intent = stripe.PaymentIntent.retrieve(order.stripe_payment_intent)

        if payment_intent['status'] == 'succeeded':
            order.paid = True
            order.save()
            return Response({'status': 'Payment successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Payment not confirmed'}, status=status.HTTP_400_BAD_REQUEST)

