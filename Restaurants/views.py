# from django.shortcuts import render

from .models import Restaurants
from .serializers import RestaurantsSerializers
from drf_yasg.utils import swagger_auto_schema
# from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from drf_yasg import openapi



class RestaurantsViewSet(viewsets.ModelViewSet):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantsSerializers





# class RestaurantsCreateView(APIView):

#  ******************code if you want to add multiple entries of data in a single request*****************
#     @swagger_auto_schema(request_body=RestaurantsSerializers)
#     def post(self, request):
#         # Check if request data is a list
#         if isinstance(request.data, list):
#             serializer = RestaurantsSerializers(data=request.data, many=True)
#         else:
#             serializer = RestaurantsSerializers(data=[request.data], many=True)
        
#         # Validate and save data
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     @swagger_auto_schema(
#         responses={200: openapi.Response("Success", RestaurantsSerializers(many=True))},
#     )
#     def get(self, request):
#         restaurants = Restaurants.objects.all()
#         serializer = RestaurantsSerializers(restaurants, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# # class RestaurantUpdateView(APIView):
#     # @swagger_auto_schema(responses={200: openapi.Response("Success", RestaurantsSerializers(many = False))},)  
#     # def get(self, request, pk):
#     #     restaurant = get_object_or_404(Restaurants, pk)
#     #     serializer = RestaurantsSerializers(restaurant, many = False)
#     #     return Response(serializer.data, status=status.HTTP_200_OK)

    
#     @swagger_auto_schema(
#         request_body=RestaurantsSerializers,
#         responses={200: openapi.Response("Success", RestaurantsSerializers)},
#     )
#     def put(self, request, pk):
#         restaurant = get_object_or_404(Restaurants, pk=pk)
#         serializer = RestaurantsSerializers(restaurant, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     @swagger_auto_schema(
#         request_body=RestaurantsSerializers,
#         responses={200: openapi.Response("Success", RestaurantsSerializers)},
#     )
#     def patch(self, request, pk):
#         restaurant = get_object_or_404(Restaurants, pk=pk)
#         serializer = RestaurantsSerializers(restaurant, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     @swagger_auto_schema(
#         responses={204: "No Content"},
#     )
#     def delete(self, request, pk):
#         restaurant = get_object_or_404(Restaurants, pk=pk)
#         restaurant.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

    
   
      
#     # @swagger_auto_schema(
#     #     responses={200: openapi.Response("Success", RestaurantsSerializers)},
#     # )
#     # def get_object(self, pk):
#     #     return get_object_or_404(Restaurants, pk=pk)


# # class RestaurantDetailView(APIView):
# #     @swagger_auto_schema(
# #         responses={200: openapi.Response("Success", RestaurantsSerializers)},
# #     )

# #     def get_object(self, pk):
# #         return get_object_or_404(Restaurants, pk)
# #     def get(self, request, pk):
# #         restaurant = self.get_object(pk)
# #         serializer = RestaurantsSerializers(restaurant)
# #         return Response(serializer.data, status=status.HTTP_200_OK)
    


