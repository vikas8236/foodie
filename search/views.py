from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from restaurants.models import Restaurant
from products.serializers import ProductSerializer
from restaurants.serializers import RestaurantSerializer

class SearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', '')

        # Search Products
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        product_results = ProductSerializer(products, many=True).data

        # Search Restaurants
        restaurants = Restaurant.objects.filter(Q(resName__icontains=query) | Q(locality__icontains=query))
        restaurant_results = RestaurantSerializer(restaurants, many=True).data

        return Response({
            'products': product_results,
            'restaurants': restaurant_results
        }, status=status.HTTP_200_OK)       

