from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Client, Sale
from .serializers import ClientSerializer, SaleSerializer

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Avg, Count, F
from django.db.models.functions import TruncDate

def index(request):
    return HttpResponse("<h1>🚀 Loja de Brinquedos API</h1><p>Bem-vindo à API da loja!</p>")

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nomeCompleto', 'email']

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client', 'data']

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def estatisticas_vendas_por_dia(request):
    vendas = (
        Sale.objects
        .values('data')
        .annotate(total=Sum('valor'))
        .order_by('data')
    )
    return Response({str(v['data']): v['total'] for v in vendas})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def estatisticas_clientes(request):

    maior_volume = (
        Sale.objects
        .values(
            'client_id',
            nome_completo=F('client__nomeCompleto')
        )
        .annotate(total=Sum('valor'))
        .order_by('-total')
        .first()
    )

    maior_media = (
        Sale.objects
        .values(
            'client_id',
            nome_completo=F('client__nomeCompleto')
        )
        .annotate(media=Avg('valor'))
        .order_by('-media')
        .first()
    )

    maior_frequencia = (
        Sale.objects
        .values(
            'client_id',
            nome_completo=F('client__nomeCompleto')
        )
        .annotate(dias=Count('data', distinct=True))
        .order_by('-dias')
        .first()
    )

    return Response({
        "maior_volume": maior_volume,
        "maior_media": maior_media,
        "maior_frequencia": maior_frequencia
    })