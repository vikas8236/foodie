
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User, Group
from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin
from user.models import User
from django.apps import apps
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


class CustomOTPAdminSite(OTPAdminSite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.register(User)
        self.register(Group)
        self.register(TOTPDevice, TOTPDeviceAdmin)
        
    def register_all_models(self):
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                try:
                    self.register(model)
                except admin.sites.AlreadyRegistered:
                    pass

admin_site = CustomOTPAdminSite(name='CustomOTPAdmin')

schema_view = get_schema_view(
    openapi.Info(
        title="Food Orering Website API",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourproject.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('restaurants/', include(('restaurants.urls', 'restaurants'), namespace='restaurants')),
    path('payment/', include('payment.urls')),
    path('voice/', include('voice.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

