from django.contrib import admin
from .models import Client, Sale

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nomeCompleto', 'email', 'dataNascimento', 'createdAt')
    list_filter = ('dataNascimento',) 
    search_fields = ('nomeCompleto', 'email') 

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('client', 'valor', 'data', 'createdAt')
    list_filter = ('data', 'client')
    search_fields = ('client__nomeCompleto',)
