from rest_framework import viewsets, permissions
from .models import Client
from .serializers import ClientSerializer
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

def index(request):
    return HttpResponse("<h1>🚀 Loja de Brinquedos API</h1><p>Bem-vindo à API da loja!</p>")

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nomeCompleto', 'email']