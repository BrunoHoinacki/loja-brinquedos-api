from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Client, Sale
import datetime

class AuthSetupMixin:
    """Mixin para configurar autenticação e cliente de teste."""
    def setUp(self):
        super().setUp() # Garante que o setUp da classe base (APITestCase) seja chamado.

        self.username = 'testuser' # Nome de usuário genérico para testes
        self.password = 'testpassword123' # Senha genérica e forte o suficiente para testes

        # Cria um superusuário para os testes de API.
        # Garante que o usuário tenha todas as permissões necessárias.
        self.user = User.objects.create_superuser(
            username=self.username,
            email='test@example.com',
            password=self.password
        )

        self.token = self.get_jwt_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def get_jwt_token(self):
        """Obtém um token JWT para o usuário de teste."""
        login_url = reverse('token_obtain_pair')
        response = self.client.post(login_url, {'username': self.username, 'password': self.password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']


class ClientAPITests(AuthSetupMixin, APITestCase):
    """Testes para a API de Clientes."""

    def setUp(self):
        super().setUp()
        self.client_data = {
            'nomeCompleto': 'João Silva',
            'email': 'joao.silva@example.com',
            'dataNascimento': '1990-01-01'
        }
        self.client_url = reverse('client-list')
        self.client_detail_url = lambda pk: reverse('client-detail', kwargs={'pk': pk})

    def test_create_client(self):
        """Deve ser possível criar um novo cliente."""
        response = self.client.post(self.client_url, self.client_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(Client.objects.get().nomeCompleto, 'João Silva')

    def test_create_client_unauthenticated(self):
        """Não deve ser possível criar um cliente sem autenticação."""
        self.client.credentials() # Remove as credenciais
        response = self.client.post(self.client_url, self.client_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_clients(self):
        """Deve ser possível listar clientes."""
        Client.objects.create(**self.client_data)
        response = self.client.get(self.client_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['nomeCompleto'], 'João Silva')

    def test_retrieve_client(self):
        """Deve ser possível obter detalhes de um cliente específico."""
        client = Client.objects.create(**self.client_data)
        response = self.client.get(self.client_detail_url(client.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nomeCompleto'], 'João Silva')

    def test_update_client_partial(self):
        """Deve ser possível atualizar parcialmente um cliente."""
        client = Client.objects.create(**self.client_data)
        update_data = {'email': 'novo.email@example.com'}
        response = self.client.patch(self.client_detail_url(client.pk), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        client.refresh_from_db()
        self.assertEqual(client.email, 'novo.email@example.com')

    def test_update_client_full(self):
        """Deve ser possível atualizar completamente um cliente."""
        client = Client.objects.create(**self.client_data)
        full_update_data = {
            'nomeCompleto': 'Maria Santos',
            'email': 'maria.santos@example.com',
            'dataNascimento': '1995-03-15'
        }
        response = self.client.put(self.client_detail_url(client.pk), full_update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        client.refresh_from_db()
        self.assertEqual(client.nomeCompleto, 'Maria Santos')
        self.assertEqual(client.email, 'maria.santos@example.com')

    def test_delete_client(self):
        """Deve ser possível deletar um cliente."""
        client = Client.objects.create(**self.client_data)
        response = self.client.delete(self.client_detail_url(client.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Client.objects.count(), 0)

    def test_filter_clients_by_name(self):
        """Deve ser possível filtrar clientes por nome."""
        Client.objects.create(nomeCompleto='Alice', email='alice@example.com', dataNascimento='2000-01-01')
        Client.objects.create(nomeCompleto='Bob', email='bob@example.com', dataNascimento='2001-01-01')
        response = self.client.get(self.client_url + '?nomeCompleto=Alice', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['nomeCompleto'], 'Alice')

    def test_filter_clients_by_email(self):
        """Deve ser possível filtrar clientes por e-mail."""
        Client.objects.create(nomeCompleto='Alice', email='alice@example.com', dataNascimento='2000-01-01')
        Client.objects.create(nomeCompleto='Bob', email='bob@example.com', dataNascimento='2001-01-01')
        response = self.client.get(self.client_url + '?email=bob@example.com', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['email'], 'bob@example.com')

class SaleAPITests(AuthSetupMixin, APITestCase):
    """Testes para a API de Vendas."""

    def setUp(self):
        super().setUp()
        self.client_obj = Client.objects.create(
            nomeCompleto='Cliente Teste',
            email='cliente.teste@example.com',
            dataNascimento='1985-06-20'
        )
        self.today_str = datetime.date.today().strftime('%Y-%m-%d')
        self.sale_data = {
            'client': self.client_obj.pk,
            'valor': '99.99',
            'data': self.today_str
        }
        self.sale_url = reverse('sale-list')
        self.sale_detail_url = lambda pk: reverse('sale-detail', kwargs={'pk': pk})


    def test_create_sale(self):
        """Deve ser possível criar uma nova venda."""
        response = self.client.post(self.sale_url, self.sale_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sale.objects.count(), 1)
        self.assertEqual(float(Sale.objects.get().valor), 99.99)
        self.assertEqual(Sale.objects.get().client.pk, self.client_obj.pk)

    def test_create_sale_unauthenticated(self):
        """Não deve ser possível criar uma venda sem autenticação."""
        self.client.credentials()
        response = self.client.post(self.sale_url, self.sale_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_sales(self):
        """Deve ser possível listar vendas."""
        Sale.objects.create(client=self.client_obj, valor=50.00, data=self.today_str)
        response = self.client.get(self.sale_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(float(response.data['results'][0]['valor']), 50.00)

    def test_retrieve_sale(self):
        """Deve ser possível obter detalhes de uma venda específica."""
        sale = Sale.objects.create(client=self.client_obj, valor=150.00, data=self.today_str)
        response = self.client.get(self.sale_detail_url(sale.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['valor']), 150.00)
        self.assertEqual(response.data['client'], self.client_obj.pk)

    def test_update_sale_partial(self):
        """Deve ser possível atualizar parcialmente uma venda."""
        sale = Sale.objects.create(client=self.client_obj, valor=200.00)
        original_sale_data_str = str(sale.data)

        update_data = {'valor': '250.75'}
        response = self.client.patch(self.sale_detail_url(sale.pk), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        sale.refresh_from_db()
        self.assertEqual(float(sale.valor), 250.75)
        self.assertEqual(str(sale.data), original_sale_data_str)

    def test_update_sale_full(self):
        """Deve ser possível atualizar completamente uma venda (exceto campos auto_now_add)."""
        sale = Sale.objects.create(client=self.client_obj, valor=100.00)
        original_sale_data_str = str(sale.data)

        new_client = Client.objects.create(
            nomeCompleto='Novo Cliente',
            email='novo@example.com',
            dataNascimento='1970-01-01'
        )
        full_update_data = {
            'client': new_client.pk,
            'valor': '300.00',
        }
        response = self.client.put(self.sale_detail_url(sale.pk), full_update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        sale.refresh_from_db()
        self.assertEqual(float(sale.valor), 300.00)
        self.assertEqual(sale.client.pk, new_client.pk)
        self.assertEqual(str(sale.data), original_sale_data_str)

    def test_delete_sale(self):
        """Deve ser possível deletar uma venda."""
        Sale.objects.create(client=self.client_obj, valor=75.00)
        response = self.client.delete(self.sale_detail_url(Sale.objects.first().pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Sale.objects.count(), 0)

    def test_filter_sales_by_client(self):
        """Deve ser possível filtrar vendas por cliente."""
        another_client = Client.objects.create(
            nomeCompleto='Outro Cliente',
            email='outro@example.com',
            dataNascimento='1999-01-01'
        )
        Sale.objects.create(client=self.client_obj, valor=10.00)
        Sale.objects.create(client=another_client, valor=20.00)
        
        response = self.client.get(self.sale_url + f'?client={self.client_obj.pk}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['client'], self.client_obj.pk)

    def test_filter_sales_by_date(self):
        """Deve ser possível filtrar vendas por data."""
        today = datetime.date.today().strftime('%Y-%m-%d')
        Sale.objects.create(client=self.client_obj, valor=10.00, data=today)
        Sale.objects.create(client=self.client_obj, valor=20.00, data=today)
        
        response = self.client.get(self.sale_url + f'?data={today}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['data'], today)