from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'nomeCompleto', 'email', 'dataNascimento', 'createdAt']
        read_only_fields = ['id', 'createdAt']
