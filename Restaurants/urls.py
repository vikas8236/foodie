from .views import RestaurantsViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers


router = DefaultRouter()
router.register(r'', RestaurantsViewSet)

urlpatterns = [
    path('restaurants/', include(router.urls)),
    # path('restaurants/', RestaurantsViewSet.as_view(), name = "create-restuarants"),
    
    # path('restaurants/<int:pk>', RestaurantUpdateView.as_view(), name = "detail-view")
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 