

from django.urls import path
from testcelery.views import test_celery

urlpatterns = [
    path('test-celery/', test_celery, name='test_celery'),
]
