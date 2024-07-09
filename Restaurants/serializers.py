from rest_framework import serializers
from .models import Restaurants


class RestaurantsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = ['id', 'resImage', 'resName', 'estimated_time','menue', 'rating', 'locality', 'offer']

       
