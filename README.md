# Projeto Loja de Brinquedos - API e Frontend

Este é um projeto full stack para gerenciar clientes e vendas de uma loja de brinquedos. O **backend é desenvolvido com Django REST Framework** para a API, e o **frontend será construído com Nuxt.js (Vue.js)** para a interface do usuário.

## Estrutura do Projeto

O projeto está organizado em um monorepo, com as seguintes pastas principais:

-   `backend/`: Contém todo o código da API Django (Python), incluindo modelos, views, serializadores, URLs e testes.
-   `frontend/`: Contém todo o código da aplicação frontend (Nuxt.js / Vue.js).
-   `venv/`: Ambiente virtual Python para isolar as dependências do backend.

---

## Como o Sistema Vai Funcionar

### Backend (API Django)

O backend será o coração do sistema, responsável por toda a lógica de negócio e persistência de dados. Ele fornecerá uma API RESTful para:

1.  **Gerenciamento de Clientes**: Permitirá o cadastro, listagem (com filtros por nome/e-mail), exclusão e edição das informações de clientes.
2.  **Gerenciamento de Vendas**: Registrará as vendas associadas a cada cliente.
3.  **Autenticação e Autorização**: Todas as rotas sensíveis serão protegidas por autenticação JWT (JSON Web Tokens), garantindo que apenas usuários autorizados possam acessá-las.
4.  **Estatísticas Avançadas**: Fornecerá endpoints para calcular e retornar:
    * O total de vendas por dia.
    * O cliente com o maior volume total de vendas.
    * O cliente com a maior média de valor por venda.
    * O cliente com o maior número de dias únicos com vendas registradas (frequência de compra).
5.  **Testes Automatizados**: Contará com uma suíte de testes para garantir a robustez e a correção das funcionalidades da API.

### Frontend (Nuxt.js)

O frontend será a interface interativa que os usuários irão interagir. Ele será responsável por:

1.  **Interface de Usuário Amigável**: Permitirá a adição de novos clientes com nome, e-mail e data de nascimento.
2.  **Listagem de Clientes Dinâmica**: Exibirá a lista de clientes, permitindo operações de edição e exclusão.
3.  **Autenticação Simplificada**: Oferecerá uma forma simples de autenticação para que o usuário possa acessar as funcionalidades protegidas da API.
4.  **Consumo e Visualização de Dados da API**:
    * Consumirá os endpoints de estatísticas do backend.
    * Exibirá um gráfico visualmente atraente com o total de vendas por dia.
    * Destacará visualmente os clientes com maior volume de vendas, maior média de valor por venda e maior frequência de compras.
5.  **Tratamento e Normalização de Dados**: Um ponto crucial será a capacidade de consumir a API de listagem de clientes (que pode retornar dados em uma estrutura "desorganizada" ou redundante) e **tratar/normalizar esses dados** antes de apresentá-los na interface.
6.  **Recurso Visual Adicional**: Para cada cliente, um campo visual indicará a primeira letra do alfabeto que ainda não apareceu no nome completo do cliente. Se todas as letras de A-Z estiverem presentes, exibirá '-'.

---

## Requisitos do Sistema

Para rodar este projeto, você precisará ter instalado:

-   **Python 3.9+** (com `pip` incluído)
-   **Node.js 16+** (para o frontend, com `npm` ou `yarn` incluído)

---

## Configuração e Execução do Backend (API Django)

Siga os passos abaixo para configurar e rodar a API:

1.  **Navegue para a pasta raiz do projeto:**
    ```bash
    cd C:\Users\Bruno\code\loja-brinquedos-api
    ```

2.  **Crie e ative o ambiente virtual Python:**
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```
    *Se você estiver usando o terminal WSL/Linux/macOS, use:*
    ```bash
    source venv/bin/activate
    ```

3.  **Navegue para a pasta do backend:**
    ```bash
    cd backend
    ```

4.  **Instale as dependências Python:**
    Com o ambiente virtual ativado (você verá `(venv)` no prompt):

    ```bash
    pip install -r requirements.txt
    ```

5.  **Realize as migrações do banco de dados:**
    ```bash
    cd toy_store_project
    python manage.py migrate
    ```

6.  **Crie um superusuário (opcional, para acessar o painel admin do Django):**
    ```bash
    python manage.py createsuperuser
    ```
    Siga as instruções para criar o usuário e senha.

7.  **Execute o servidor de desenvolvimento Django:**
    ```bash
    python manage.py runserver
    ```
    A API estará disponível em `http://127.0.0.1:8000/`.

---

## Configuração e Execução do Frontend (Nuxt.js)

Siga os passos abaixo para configurar e rodar a aplicação frontend:

1.  **Navegue para a pasta do frontend:**
    ```bash
    cd C:\Users\Bruno\code\loja-brinquedos-api\frontend
    ```

2.  **Instale as dependências JavaScript:**
    (Este passo será realizado após a criação do projeto Nuxt.js)
    ```bash
    # npm install
    ```

3.  **Inicie a aplicação frontend:**
    (Este passo será realizado após a criação do projeto Nuxt.js)
    ```bash
    # npm run dev
    ```
    A aplicação geralmente será aberta em `http://localhost:3000/` (ou outra porta).

---

## Testes

### Backend
Para rodar os testes automatizados do backend:

1.  Ative o ambiente virtual e navegue para a pasta `backend`.
2.  Execute:
    ```bash
    python manage.py test
    ```

### Frontend
(Instruções de teste para Nuxt.js serão adicionadas após a implementação do frontend)

---

## Desafio: Detalhes da Implementação

Este projeto visa avaliar o domínio de stack, boas práticas, raciocínio lógico e estruturação, com os seguintes pontos chave a serem abordados:

### Para o Backend (API Django):
-   Permitir cadastrar clientes de uma loja de brinquedos (nome, e-mail, data de nascimento).
-   Listar os clientes com opções de filtros (por nome ou e-mail).
-   Permitir deletar um cliente.
-   Permitir editar informações de um cliente.
-   **Requer autenticação (JWT) para acessar as rotas.**
-   **Adicionar testes automatizados.**
-   Criar uma tabela adicional chamada `Sales` para armazenar vendas por cliente.
-   Criar uma rota de estatísticas que retorne o total de vendas por dia.
-   Criar outra rota que retorne:
    -   O cliente com o maior volume de vendas.
    -   O cliente com a maior média de valor por venda.
    -   O cliente com o maior número de dias únicos com vendas registradas (frequência de compra).
-   **Banco de dados obrigatório no backend.**

### Para o Frontend (Nuxt.js):
-   Permitir adicionar clientes com nome, e-mail e data de nascimento.
-   Listar os campos conforme achar pertinente.
-   **Adicionar autenticação simples.**
-   Consumir a API de estatísticas para:
    -   Exibir um gráfico com o total de vendas por dia.
    -   Destacar visualmente:
        -   O cliente com maior volume de vendas.
        -   O cliente com maior média de valor por venda.
        -   O cliente com maior frequência de compras.
-   Adicionar um campo visual que indique, para cada cliente, a primeira letra do alfabeto que ainda não apareceu no nome completo do cliente. Se todas as letras de a-z estiverem presentes, exibir '-'.
-   **Ao consumir a API de listagem de clientes, considerar que o endpoint pode retornar uma estrutura desorganizada ou com dados redundantes.** O formato exato do JSON a ser tratado no front-end é:
    ```json
    {
        "data": {
            "clientes": [
                {
                    "info": {
                        "nomeCompleto": "Ana Beatriz",
                        "detalhes": {
                            "email": "ana.b@example.com",
                            "nascimento": "1992-05-01"
                        }
                    },
                    "estatisticas": {
                        "vendas": [
                            {
                                "data": "2024-01-01",
                                "valor": 150
                            },
                            {
                                "data": "2024-01-02",
                                "valor": 50
                            }
                        ]
                    }
                },
                {
                    "info": {
                        "nomeCompleto": "Carlos Eduardo",
                        "detalhes": {
                            "email": "cadu@example.com",
                            "nascimento": "1987-08-15"
                        }
                    },
                    "duplicado": {
                        "nomeCompleto": "Carlos Eduardo"
                    },
                    "estatisticas": {
                        "vendas": []
                    }
                }
            ]
        },
        "meta": {
            "registroTotal": 2,
            "pagina": 1
        },
        "redundante": {
            "status": "ok"
        }
    }
    ```
    O candidato deve extrair corretamente os dados relevantes e ignorar as informações desnecessárias ou duplicadas.