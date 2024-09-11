
# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import Restaurant, MenuItem
# from .serializers import RestaurantSerializer, MenuItemSerializer

# class RestaurantListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer

# class RestaurantRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer

# class MenuItemListCreateAPIView(generics.ListCreateAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer

#     def get_queryset(self):
#         restaurant_id = self.kwargs['restaurant_id']
#         return MenuItem.objects.filter(restaurant_id=restaurant_id)

#     def perform_create(self, serializer):
#         restaurant_id = self.kwargs['restaurant_id']
#         restaurant = Restaurant.objects.get(id=restaurant_id)
#         serializer.save(restaurant=restaurant)
from rest_framework import generics
from .models import Restaurant, MenuItem
from .serializers import RestaurantSerializer, MenuItemSerializer

class RestaurantListCreateAPIView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class RestaurantRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class MenuItemListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return MenuItem.objects.filter(restaurant_id=restaurant_id)

    def perform_create(self, serializer):
        restaurant_id = self.kwargs['restaurant_id']
        restaurant = Restaurant.objects.get(id=restaurant_id)
        serializer.save(restaurant=restaurant)
