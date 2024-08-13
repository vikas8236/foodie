
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views import View
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from user.models import User
from products.models import Product
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi 

@method_decorator(csrf_exempt, name='dispatch')
class VoiceHelpAPIView(View):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,      
        ),
        responses={201: 'Created'}
    )
    def post(self, request, *args, **kwargs):
        to_phone = request.POST.get('to')
        if not to_phone:
            return JsonResponse({'error': 'Phone number is required'}, status=400)

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        call = client.calls.create(
            to=to_phone,
            from_=settings.TWILIO_PHONE_NUMBER,
            url=request.build_absolute_uri('/voice/voice-response/')
        )
        return JsonResponse({'call_sid': call.sid})

@method_decorator(csrf_exempt, name='dispatch')
class VoiceResponseAPIView(View):
    def get(self, request, *args, **kwargs):
        return self.handle_voice_response(request)
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,      
        ),
        responses={201: 'Created'}
    )

    def post(self, request, *args, **kwargs):
        return self.handle_voice_response(request)

    def handle_voice_response(self, request):
        response = VoiceResponse()
        response.say("Welcome to the Food Ordering Service. Please enter your mobile number for authentication.")
        response.gather(
            input='dtmf',
            numDigits=10,
            action='/voice/receive-mobile-number/',
            method='POST'
        )
        return HttpResponse(response.to_xml(), content_type='application/xml')

@method_decorator(csrf_exempt, name='dispatch')
class ReceiveMobileNumberAPIView(View):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,      
        ),
        responses={201: 'Created'}
    )
    def post(self, request, *args, **kwargs):
        mobile_no = request.POST.get('Digits')
        response = VoiceResponse()

        if not mobile_no or len(mobile_no) != 10:
            response.say("Invalid mobile number. Please try again.")
        
            return HttpResponse(response.to_xml(), content_type='application/xml')

        try:
            user = User.objects.get(mobile_no=mobile_no)
            token = Token.objects.get(user=user).key
            request.session['mobile_no'] = mobile_no
            request.session['auth_token'] = token

            response.say("Authentication successful. Press 1 to know available foods, Press 2 to add foods to your cart, Press 3 to view cart, press 4 to end call.")
            response.gather(
                numDigits=1,
                action='/voice/process-response/',
                method='POST'
            )
        except User.DoesNotExist:
            response.say("Mobile number not recognized. Please try again.")
        

        return HttpResponse(response.to_xml(), content_type='application/xml')

@method_decorator(csrf_exempt, name='dispatch')
class ProcessResponseAPIView(View):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,      
        ),
        responses={201: 'Created'}
    )
    def post(self, request, *args, **kwargs):
        digit = request.POST.get('Digits')
        response = VoiceResponse()

        if digit == '1':
            product_list = self.get_product_list()
            response.say(f"You selected to know the list of available foods. {product_list}")
        
        elif digit == '2':   
            response.say("You selected to add foods to your cart. Press 1 for Biriyani, Press 2 for Cakes., press 3 for kebabs, 4 for paratha, press 5 for pav bhaji, press 6 for burger, press 7 for ice cream")
            response.gather(
                numDigits=1,
                action='/voice/receive-product-selection/',
                method='POST'
            )
        
        elif digit == '3':
            response.say(" You selected to retrieve your cart,Retrieving your cart...")
            cart_contents = self.view_cart(request)
            response.say(f"Your cart contains: {cart_contents}")
            
        elif digit == '4':
            response.say("Thank you for your call. Goodbye!")
            response.hangup()
        else:
            response.say("Invalid option. Please try again.")
        

        return HttpResponse(response.to_xml(), content_type='application/xml')

    def get_product_list(self):
        client = APIClient()
        response = client.get('/products/products/')

        if response.status_code == 200:
            try:
                product_data = response.json()
                product_list = ", ".join([f"{product['name']} - {product['price']}" for product in product_data])
                return product_list if product_list else "No products available."
            except ValueError:
                return "Error parsing the product list. Please try again."
        else:
            return "There was an error retrieving the product list. Please try again."

    def view_cart(self, request):
        client = APIClient()
        user = User.objects.get(mobile_no=request.session.get('mobile_no'))
        token = request.session.get('auth_token')
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        response = client.get('/user/cart/')
        if response.status_code == 200:
            try:
                cart_data = response.json()
                item_details = []
                for item in cart_data:
                    product = item.get('product', {})
                    name = product.get('name', 'Unnamed item')
                    price = product.get('price', 'Unknown price')
                    quantity = item.get('quantity', 'Unknown quantity')
                    item_details.append(f"{name} (Quantity: {quantity}, Price: {price})")

                return ", ".join(item_details) if item_details else "Your cart is empty."
            except ValueError:
                return "Error parsing the cart response. Please try again."
        else:
            return "There was an error retrieving your cart. Please try again."

@method_decorator(csrf_exempt, name='dispatch')
class ReceiveProductSelectionAPIView(View):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,      
        ),
        responses={201: 'Created'}
    )
    def post(self, request, *args, **kwargs):
        product_selection = request.POST.get('Digits')
        response = VoiceResponse()
        mobile_no = request.session.get('mobile_no')

        if not mobile_no:
            response.say("You need to enter your mobile number first.")
            response.redirect('/voice/process-response/')
            return HttpResponse(response.to_xml(), content_type='application/xml')

        product_mapping = {
            '1': 'Biriyani',
            '2': 'Cake',
            '3': 'Kebabs',
            '4': 'Paratha',
            '5': 'Pav Bhaji',
            '6': 'pizza',
            '7': 'Ice Cream',
            '8': 'rasgulla',
        }

        product_name = product_mapping.get(product_selection)

        if product_name:
            request.session['product_name'] = product_name
            response.say(f"You selected {product_name}. Please provide the quantity.")
            response.gather(
                input='dtmf',
                numDigits=1,
                action='/voice/receive-quantity/',
                timeout=10,
                method='POST'
            )
        else:
            response.say("Invalid selection. Please try again.")
        

        return HttpResponse(response.to_xml(), content_type='application/xml')

@method_decorator(csrf_exempt, name='dispatch')
class ReceiveQuantityAPIView(View):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,      
        ),
        responses={201: 'Created'}
    )
    def post(self, request, *args, **kwargs):
        quantity = request.POST.get('Digits')
        product_name = request.session.pop('product_name', None)
        mobile_no = request.session.get('mobile_no')

        response = VoiceResponse()

        if not mobile_no:
            response.say("You need to enter your mobile number first.")
            response.redirect('/voice/process-response/')
            return HttpResponse(response.to_xml(), content_type='application/xml')

        if quantity and product_name:
            add_to_cart_message = self.add_to_cart(request, product_name, quantity)
            response.say(f"You selected to add {product_name} with quantity {quantity} to your cart. {add_to_cart_message}")
        else:
            response.say("No quantity received or product name missing. Please try again.")
        

        return HttpResponse(response.to_xml(), content_type='application/xml')

    def add_to_cart(self, request, product_name, quantity):
        client = APIClient()
        user = User.objects.get(mobile_no=request.session.get('mobile_no'))
        token = request.session.get('auth_token')
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        product = Product.objects.get(name=product_name)
        product_id = product.id

        response = client.post('/user/add-to-cart/', {
            'product_id': product_id,
            'quantity': quantity
        })

        if response.status_code == 200:
            return "Your order has been placed successfully."
        else:
            return "There was an error placing your order. Please try again."
   
