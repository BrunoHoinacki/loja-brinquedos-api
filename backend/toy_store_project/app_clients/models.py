from django.db import models
from django.core.validators import MinValueValidator

class Client(models.Model):
    nomeCompleto = models.CharField(max_length=255, verbose_name="Nome Completo")
    
    email = models.EmailField(unique=True, verbose_name="E-mail")
    
    dataNascimento = models.DateField(verbose_name="Data de Nascimento")
    
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nomeCompleto'] 

    def __str__(self):
        return self.nomeCompleto

class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='sales', verbose_name="Cliente")
    
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Valor da Venda")
    
    data = models.DateField(auto_now_add=True, verbose_name="Data da Venda")
    
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Data de Registro")

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        ordering = ['-data', '-createdAt']

    def __str__(self):
        return f"Venda de R${self.valor:.2f} para {self.client.nomeCompleto} em {self.data.strftime('%d/%m/%Y')}"