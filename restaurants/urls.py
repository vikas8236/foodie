
from django.urls import path
from .views import (
    RestaurantListCreateAPIView,
    RestaurantRetrieveUpdateDestroyAPIView,
    MenuItemListCreateAPIView
)

urlpatterns = [
    path('restaurants/', RestaurantListCreateAPIView.as_view(), name='restaurant-list-create'),
    path('restaurants/<int:pk>/', RestaurantRetrieveUpdateDestroyAPIView.as_view(), name='restaurant-detail'),
    path('restaurants/<int:restaurant_id>/menu_items/', MenuItemListCreateAPIView.as_view(), name='menuitem-list-create'),
]
