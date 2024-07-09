from django.shortcuts import render
from user.models import User, CartItem
from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializers import UserSerializer, LoginSerializer, CartItemSerializer, CustomUserSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
# from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.response import Response

from .models import Cart
from products.models import Product
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404


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

from .serializers import LoginSerializer
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
    

class Logout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass  






