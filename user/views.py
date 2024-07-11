# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.authentication import JWTAuthentication
from user.models import User, CartItem
from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializers import UserSerializer, LoginSerializer, CartItemSerializer, CustomUserSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.response import Response
from .utils import generate_otp
from django.core.cache import cache
from django.contrib.auth import authenticate
from .models import Cart
from products.models import Product
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404   

# Register api
class UserSignupView(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        try:
            User.objects.get(email=email)
            return Response('Email already exists')
        except User.DoesNotExist:
            serializer = UserSerializer(data=request.data, context = {"request": request})
            if serializer.is_valid():
                user = serializer.save()
                user.set_password(request.data.get('password'))
                user.save()
                serializer_data = {'message': 'Register Successfully', 'data': serializer.data}
                return Response(serializer_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


import logging

logger = logging.getLogger(__name__)


#  Login api 
class LoginView(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')
                user = authenticate(email=email, password=password)
                if user:
                    # Generate or fetch existing token for the user
                    token, created = Token.objects.get_or_create(user=user)  # Use Token.objects to create or retrieve tokens
                    return Response({
                        'email': user.email,
                        'message': 'Login Successful',
                        'token': token.key,  # Send the token key to the client
                    }, status=status.HTTP_200_OK)
                else:
                    return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Exception occurred in LoginView: {e}")
            return Response("Internal server error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# cartlist api
class CartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def get(self, request):
        cart_items = self.get_queryset()
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
            cart_item = CartItem.objects.get(cart=cart, id=pk)
            cart_item.delete()
            return Response({"detail": "Item removed from cart."}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"detail": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)

# add-to-cart api
class AddToCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity', 1)  # Default to 1 if quantity not provided
            product = get_object_or_404(Product, pk=product_id)
            
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            
            if not created:
                cart_item.quantity += int(quantity)
            else:
                cart_item.quantity = int(quantity)
            cart_item.save()
            
            response_data = {
                'message': f"{product.name} added to cart",
                'email': request.user.email  # Include user's email in the response
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response("Product not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


# Profile api
class DetailProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
            return get_object_or_404(User, email=self.request.user.email)

    def get(self, request):
            user = self.get_object()
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)

    def put(self, request):
            user = self.get_object()
            serializer = CustomUserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
    
    def patch(self, request):
            user = self.get_object()
            serializer = CustomUserSerializer(user, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
    
# logout api
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request.auth.delete()
        return Response({'message': 'Logged out successfully'}, status=200)
    
# reset-password api
class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
  
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "No user is associated with this email address."}, status=status.HTTP_404_NOT_FOUND)
        
        otp = generate_otp()
        print(otp)
        # import pdb; pdb.set_trace()
        cache.set(f'password_reset_otp_{email}', otp, timeout=60)
      

        subject = "Password Reset OTP"
        message = f"Your OTP for password reset is {otp}."
        send_mail(subject, message, 'admin@example.com', [email])

        return Response({"detail": "OTP has been sent to your email."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']
        cached_otp = cache.get(f'password_reset_otp_{email}')

        if cached_otp is None or cached_otp != otp:
            return Response({"detail": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "No user is associated with this email address."}, status=status.HTTP_404_NOT_FOUND)
        
        user.set_password(new_password)
        user.save()

        cache.delete(f'password_reset_otp_{email}')

        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)







