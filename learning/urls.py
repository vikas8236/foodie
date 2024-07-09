"""
URL configuration for learning project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for learning project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

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

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('restaurants/', include(('Restaurants.urls', 'Restaurants'), namespace='restaurants')),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)