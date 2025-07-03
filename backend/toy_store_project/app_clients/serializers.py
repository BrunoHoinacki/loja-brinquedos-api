from rest_framework import serializers
from .models import Client, Sale

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'nomeCompleto', 'email', 'dataNascimento', 'createdAt']
        read_only_fields = ['id', 'createdAt']

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id', 'client', 'valor', 'data', 'createdAt']
        read_only_fields = ['id', 'createdAt']