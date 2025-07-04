from rest_framework.routers import DefaultRouter
from .views import (
    ClientViewSet, SaleViewSet,
    estatisticas_vendas_por_dia, estatisticas_clientes
)
from django.urls import path, include

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'sales', SaleViewSet, basename='sale')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/vendas-por-dia/', estatisticas_vendas_por_dia, name='estatisticas_vendas'),
    path('stats/clientes/', estatisticas_clientes, name='estatisticas_clientes'),
]