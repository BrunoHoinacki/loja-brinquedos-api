from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, SaleViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'sales', SaleViewSet, basename='sale')

urlpatterns = [
    path('', include(router.urls)),   
]