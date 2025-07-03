from rest_framework.routers import DefaultRouter
from .views import ClientViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')

urlpatterns = [
    path('', include(router.urls)),
]