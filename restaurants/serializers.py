
from rest_framework import serializers
from .models import Restaurant, MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'productName', 'price', 'description', 'productImage']

class RestaurantSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'resImage', 'resName', 'estimated_time', 'rating', 'locality', 'offer', 'menu_items']
