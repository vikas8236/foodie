
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
import stripe
from .models import Payment
from .serializers import PaymentSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeWebhookView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,      
        ),
        responses={201: 'Created'}
    )
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE',None)
        endpoint_secret = settings.WEBHOOK_SECRET_KEY
        print("stripe-signature:",sig_header)
        if sig_header is None:
            print("Missing Stripe signature header")
            return Response({'error': 'Missing Stripe signature header'}, status=400)

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            print(f"Invalid payload: {e}")
            return Response({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            print(f"Invalid signature: {e}")
            return Response({'error': 'Invalid signature'}, status=400)

        # Handle event types
        if event['type'] == 'payment_intent.succeeded':
            intent = event['data']['object']
            try:
                payment = Payment.objects.get(stripe_payment_intent_id=intent['id'])
                payment.status = 'succeeded'
                payment.save()
                print(f"Payment {intent['id']} succeeded")
            except Payment.DoesNotExist:
                print(f"Payment with intent id {intent['id']} not found")
        elif event['type'] == 'payment_intent.payment_failed':
            intent = event['data']['object']
            try:
                payment = Payment.objects.get(stripe_payment_intent_id=intent['id'])
                payment.status = 'failed'
                payment.save()
                print(f"Payment {intent['id']} failed")
            except Payment.DoesNotExist:
                print(f"Payment with intent id {intent['id']} not found")

        return Response({'status': 'success'}, status=200)


class StripeCheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,      
        ),
        responses={201: 'Created'}
    )
    def post(self, request, *args, **kwargs):
        try:
            # Create a PaymentIntent on Stripe
            intent = stripe.PaymentIntent.create(
                amount=request.data['amount'] * 100,
                currency=request.data['currency'],
                payment_method_types=request.data.get('payment_method_types', ['card']),
            )

            # Save initial payment information to the database using the serializer
            payment_data = {
                'user': request.user.id,
                'stripe_payment_intent_id': intent.id,
                'amount': request.data['amount'],
                'currency': request.data['currency'],
                'status': intent.status,
            }

            serializer = PaymentSerializer(data=payment_data)
            if serializer.is_valid():
                payment = serializer.save()
            else:
                print(f"Payment serializer errors: {serializer.errors}")
                return Response(serializer.errors, status=400)

            # Retrieve the PaymentIntent to check its final status
            final_intent = stripe.PaymentIntent.retrieve(intent.id)
            payment.status = final_intent.status
            print(payment.status)
            payment.save()
            print(payment)

            return Response({
                'clientSecret': intent.client_secret,
            })
        except Exception as e:
            print(f"Error in StripeCheckoutView: {e}")
            return Response({
                'error': str(e)
            }, status=500)
