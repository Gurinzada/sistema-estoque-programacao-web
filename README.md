<p align="center">
  <img src="https://img.icons8.com/fluency/96/box.png" width="100" alt="Estoque"/>
</p>

<h1 align="center"> 📊 Sistema de Gerenciamento de Estoque 📦</h1>

<p align="center">
  <i>Disciplina: GAC116 - Programação WEB</i><br>
  <i>Universidade Federal de Lavras (UFLA)</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-em%20desenvolvimento-yellow" alt="Status do Projeto"/>
  <img src="https://img.shields.io/badge/python-3.13.2-blue.svg" alt="Python Version"/>
  <img src="https://img.shields.io/badge/django-5.2.7-green.svg" alt="Django Version"/>
  <img src="https://img.shields.io/badge/DRF-3.14+-orange.svg" alt="Django REST Framework"/>
</p>

---
## 👨‍💻 Equipe

- **Professor:** Raphael Winckler de Bettio
- **Alunos:** Augusto Inácio Silva Mariano e Érika Mara de Morais Machado

---

# 📌 Sobre o Projeto

O Sistema de Gerenciamento de Estoque é uma aplicação web completa desenvolvida com Django e Django REST Framework, que permite o controle eficiente de produtos, categorias, fornecedores e movimentações de estoque. O sistema oferece autenticação segura (via email/senha e Google OAuth), interface web moderna e API RESTful para integração.

##  🎯 1º CheckPoint
```
⚠️ Esta primeira etapa do projeto focou na definição da estrutura do banco de dados e modelagem do ambiente administrativo, preparando para futuras integrações, regras de negócio e funcionalidades mais complexas.
```

##  🎯 2º CheckPoint
```
✅ Implementação completa da API REST, autenticação JWT, autenticação Google OAuth, interface web com HTML/CSS/JavaScript, sistema de gerenciamento completo com dashboards e relatórios.
```

O projeto evoluiu de uma modelagem inicial para uma aplicação completa com:
- **Backend RESTful**: API completa para todas as operações CRUD
- **Autenticação Robusta**: Login tradicional e integração com Google
- **Interface Web**: Templates HTML com CSS e JavaScript para gerenciamento visual
- **Relatórios**: Dashboard com métricas e análises de estoque
- **Soft Delete**: Implementação de exclusão lógica para preservação de dados históricos

--- 
##  🎯 Objetivos

- ✔ Permitir cadastro e gestão de produtos, categorias, fornecedores e usuários
- ✔ Registrar movimentações de estoque (entrada/saída) associadas a produtos e usuários
- ✔ Disponibilizar interface administrativa via Django Admin
- ✔ Fornecer API RESTful completa para todas as operações
- ✔ Implementar autenticação segura com JWT e Google OAuth
- ✔ Criar interface web moderna para gerenciamento do sistema
- ✔ Gerar relatórios e métricas de estoque
  
--- 
## 🔧 Principais Funcionalidades

### Autenticação e Autorização
- ✔ Login com email e senha
- ✔ Autenticação OAuth 2.0 com Google
- ✔ Sistema de permissões baseado em roles (Admin/Colaborador)
- ✔ Tokens JWT com refresh token
- ✔ Sessões seguras com controle de estado

### Gerenciamento de Produtos
- ✔ CRUD completo de produtos via API e interface web
- ✔ Associação de produtos com categorias
- ✔ Controle de preços (custo e venda)
- ✔ Rastreamento de quantidade em estoque
- ✔ Soft delete para preservação de histórico
- ✔ Contagem de produtos por categoria

### Gerenciamento de Categorias
- ✔ CRUD de categorias
- ✔ Relacionamento com produtos
- ✔ Validação de unicidade

### Gerenciamento de Fornecedores
- ✔ CRUD completo de fornecedores
- ✔ Relacionamento N:N com produtos
- ✔ Validação de CNPJ e email únicos
- ✔ Controle de endereço e contato

### Movimentações de Estoque
- ✔ Registro de entradas e saídas
- ✔ Rastreamento por usuário responsável
- ✔ Histórico completo de movimentações
- ✔ Cálculo de lucro em saídas
- ✔ Relatórios de entradas e saídas

### Gerenciamento de Usuários
- ✔ Sistema de autenticação personalizado
- ✔ Gerenciamento de perfis (Admin/Colaborador)
- ✔ CRUD de usuários com validações
- ✔ Soft delete de usuários

### Interface Web
- ✔ Dashboard com métricas e gráficos
- ✔ Página de login responsiva
- ✔ Gerenciamento de estoque via interface
- ✔ Gerenciamento de fornecedores
- ✔ Gerenciamento de usuários
- ✔ Design moderno e intuitivo

<p align="center">
  
![Modelagem BD](https://github.com/user-attachments/assets/fbfdab13-a605-4cee-8fb3-fe565b24cad6)

</p>

---

## 📡 API REST Endpoints

### Autenticação
- `POST /api/login` - Login com email e senha
- `GET /api/login/google` - Iniciar autenticação Google OAuth
- `GET /api/login/google/callback` - Callback OAuth do Google
- `GET /api/me` - Obter dados do usuário autenticado

### Usuários
- `GET /api/users` - Listar todos os usuários
- `POST /api/users` - Criar novo usuário
- `GET /api/users/<id>` - Obter detalhes de um usuário
- `PUT /api/users/<id>` - Atualizar usuário
- `DELETE /api/users/<id>` - Remover usuário (soft delete)

### Produtos
- `GET /api/products` - Listar todos os produtos
- `POST /api/products` - Criar novo produto
- `GET /api/products/<id>` - Obter detalhes de um produto
- `PUT /api/products/<id>` - Atualizar produto
- `DELETE /api/products/<id>` - Remover produto (soft delete)
- `GET /api/products/count` - Contar produtos por categoria

### Categorias
- `GET /api/category` - Listar todas as categorias
- `POST /api/category` - Criar nova categoria
- `GET /api/category/<id>` - Obter detalhes de uma categoria
- `PUT /api/category/<id>` - Atualizar categoria
- `DELETE /api/category/<id>` - Remover categoria

### Fornecedores
- `GET /api/suppliers` - Listar todos os fornecedores
- `POST /api/suppliers` - Criar novo fornecedor
- `GET /api/suppliers/<id>` - Obter detalhes de um fornecedor
- `PUT /api/suppliers/<id>` - Atualizar fornecedor
- `DELETE /api/suppliers/<id>` - Remover fornecedor (soft delete)

### Movimentações de Estoque
- `GET /api/stock/movements` - Listar movimentações
- `POST /api/stock/movements` - Criar nova movimentação
- `GET /api/stock/movements/<id>` - Obter detalhes de uma movimentação
- `PUT /api/stock/movements/<id>` - Atualizar movimentação
- `DELETE /api/stock/movements/<id>` - Remover movimentação
- `GET /api/stock/profit` - Obter relatório de lucro
- `GET /api/stock/out-and-in` - Obter relatório de entradas e saídas

### Páginas Web
- `GET /` - Página de login
- `GET /dashboard` - Dashboard principal
- `GET /stock` - Gerenciamento de estoque
- `GET /users` - Gerenciamento de usuários
- `GET /suppliers` - Gerenciamento de fornecedores

---

## ⚙️ Tecnologias Utilizadas

### Backend
- **Python 3.13.2** - Linguagem de programação
- **Django 5.2.7** - Framework web
- **Django REST Framework** - Criação de APIs RESTful
- **Django REST Framework SimpleJWT** - Autenticação JWT
- **SQLite** - Banco de dados padrão (com suporte opcional para MySQL)

### Autenticação e Segurança
- **Google Auth** - Autenticação OAuth com Google
- **Google Auth OAuthLib** - Cliente OAuth2 para Google
- **JWT (JSON Web Tokens)** - Tokens de autenticação seguros
- **Python Dotenv** - Gerenciamento de variáveis de ambiente

### Frontend
- **HTML5** - Estrutura das páginas
- **CSS3** - Estilização
- **JavaScript (Vanilla)** - Interatividade e consumo da API

### Arquitetura
- **Model-View-Service (MVS)** - Separação de lógica de negócios
- **REST API** - Comunicação cliente-servidor
- **Custom User Model** - Sistema de autenticação personalizado

## 🚀 Como Usar?

### � Pré-requisitos

- Python 3.13.2 ou superior
- Git
- Conta Google (para autenticação OAuth - opcional)

### �📥 Instalação

1. Clone o repositório e acesse a pasta do projeto:

```powershell
git clone https://github.com/Gurinzada/sistema-estoque-programacao-web
cd sistema-estoque-programacao-web
```

2. Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

3. Instale as dependências:

```powershell
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente (opcional - para Google OAuth):

Crie um arquivo `.env` na raiz do projeto com:

```env
GOOGLE_CLIENT_ID=seu_client_id
GOOGLE_CLIENT_SECRET=seu_client_secret
GOOGLE_CLIENT_SECRETS_FILE=caminho_para_arquivo_secrets.json
GOOGLE_REDIRECT_URI=http://127.0.0.1:8000/api/login/google/callback
```

### ⚙️ Configuração do Banco de Dados

1. Aplique as migrations:

```powershell
python manage.py migrate
```

2. Crie usuários administradores iniciais (opcional):

```powershell
python manage.py seed_admins
```

3. Ou crie um superusuário manualmente:

```powershell
python manage.py createsuperuser
```

### ▶️ Execução

1. Inicie o servidor de desenvolvimento:

```powershell
python manage.py runserver
```

2. Acesse as páginas:
   - **Página de Login**: `http://127.0.0.1:8000/`
   - **Dashboard**: `http://127.0.0.1:8000/dashboard` (requer autenticação)
   - **Django Admin**: `http://127.0.0.1:8000/admin/`
   - **API**: `http://127.0.0.1:8000/api/`

### 🔐 Autenticação

O sistema oferece duas formas de autenticação:

1. **Email e Senha**:
   - Use o formulário de login na página inicial
   - Credenciais criadas via `createsuperuser` ou `seed_admins`

2. **Google OAuth**:
   - Configure as credenciais do Google Cloud Console
   - Clique em "Login com Google" na página de login

### 🧪 Testando a API

Você pode testar a API usando ferramentas como Postman, Insomnia ou cURL:

```powershell
# Login
curl -X POST http://127.0.0.1:8000/api/login -H "Content-Type: application/json" -d '{"email":"seu@email.com","password":"suasenha"}'

# Listar produtos (requer token JWT)
curl -X GET http://127.0.0.1:8000/api/products -H "Authorization: Bearer seu_token_jwt"
```

## 📂 Estrutura do Projeto

```bash
sistema-estoque-programacao-web/
├─ 📄 db.sqlite3                          # Banco de dados SQLite
├─ 📄 manage.py                           # Script de gerenciamento Django
├─ � requirements.txt                    # Dependências do projeto
├─ 📄 README.md                           # Documentação do projeto
├─ 📄 client_secret_*.json                # Credenciais Google OAuth (não versionado)
│
├─ �📁 estoque/                            # App principal do Django
│  ├─ 📄 admin.py                         # Configuração do Django Admin
│  ├─ 📄 apps.py                          # Configuração da aplicação
│  ├─ 📄 models.py                        # Modelos de dados (User, Product, Category, Supplier, MovementStock)
│  ├─ � urls.py                          # Rotas da API e páginas web
│  │
│  ├─ �📁 management/                      # Comandos customizados
│  │  └─ 📁 commands/
│  │     ├─ 📄 __init__.py
│  │     └─ 📄 seed_admins.py            # Comando para criar admins iniciais
│  │
│  ├─ 📁 migrations/                      # Migrations do banco de dados
│  │  ├─ 📄 0001_initial.py              # Criação das tabelas iniciais
│  │  ├─ 📄 0002_alter_movementstock_*.py # Ajustes no modelo MovementStock
│  │  ├─ 📄 0003_alter_category_options.py # Ajustes em Category
│  │  └─ 📄 0004_user_groups_*.py        # Implementação do User customizado
│  │
│  ├─ 📁 services/                        # Camada de lógica de negócios
│  │  ├─ 📄 google_auth_service.py       # Serviço de autenticação Google OAuth
│  │  ├─ 📄 product_service.py           # Lógica de negócio de produtos
│  │  ├─ 📄 stock_service.py             # Lógica de movimentações de estoque
│  │  ├─ 📄 supplier_service.py          # Lógica de fornecedores
│  │  └─ 📄 user_service.py              # Lógica de usuários e autenticação
│  │
│  ├─ 📁 static/estoque/                  # Arquivos estáticos (CSS, JS)
│  │  ├─ 📁 scripts/                     # JavaScript
│  │  │  ├─ 📄 dashboard.js              # Lógica do dashboard
│  │  │  ├─ 📄 login.js                  # Lógica de login
│  │  │  ├─ 📄 stock.js                  # Gerenciamento de estoque
│  │  │  ├─ 📄 supplier.js               # Gerenciamento de fornecedores
│  │  │  └─ 📄 users.js                  # Gerenciamento de usuários
│  │  │
│  │  └─ 📁 styles/                      # CSS
│  │     ├─ 📄 dashboard.css             # Estilos do dashboard
│  │     ├─ 📄 login.css                 # Estilos de login
│  │     ├─ 📄 stock.css                 # Estilos de estoque
│  │     ├─ 📄 supplier.css              # Estilos de fornecedores
│  │     └─ 📄 users.css                 # Estilos de usuários
│  │
│  ├─ 📁 templates/estoque/               # Templates HTML
│  │  ├─ 📄 dashboard.html               # Dashboard principal
│  │  ├─ 📄 login.html                   # Página de login
│  │  ├─ 📄 stock.html                   # Gerenciamento de estoque
│  │  ├─ 📄 suppliers.html               # Gerenciamento de fornecedores
│  │  └─ 📄 users.html                   # Gerenciamento de usuários
│  │
│  └─ 📁 views/                           # Views (controladores)
│     ├─ 📄 __init__.py
│     ├─ 📄 auth_view.py                 # Views de autenticação
│     ├─ 📄 product_view.py              # Views de produtos e categorias
│     ├─ 📄 stock_view.py                # Views de movimentações
│     ├─ 📄 supplier_view.py             # Views de fornecedores
│     └─ 📄 user_view.py                 # Views de usuários
│
└─ 📁 sistema_estoque/                    # Configurações do projeto Django
   ├─ 📄 __init__.py
   ├─ 📄 asgi.py                          # Configuração ASGI
   ├─ 📄 settings.py                      # Configurações principais (DB, Apps, Auth, JWT)
   ├─ 📄 urls.py                          # URLs principais do projeto
   └─ 📄 wsgi.py                          # Configuração WSGI
```

---

## 🗄️ Modelos de Dados

### User (Usuário Customizado)
- **Campos**: id, name, jobTitle, role (ADMIN/COLLABORATOR), email, password, is_active, is_staff, createdAt, updatedAt, deletedAt
- **Autenticação**: Usa email como USERNAME_FIELD
- **Manager Customizado**: UserManager com métodos create_user e create_superuser

### Category (Categoria)
- **Campos**: id, name, description
- **Relacionamento**: One-to-Many com Product

### Product (Produto)
- **Campos**: id, name, description, quatityStock, costPrice, salePrice, categoryId, createdAt, updatedAt, deletedAt
- **Relacionamento**: 
  - Many-to-One com Category
  - Many-to-Many com Supplier
  - One-to-Many com MovementStock

### Supplier (Fornecedor)
- **Campos**: id, name, cnpj, email, phone, address, zipCode, products, createdAt, updatedAt, deletedAt
- **Relacionamento**: Many-to-Many com Product

### MovementStock (Movimentação de Estoque)
- **Campos**: id, type (ENTRADA/SAIDA), date, quantity, product, user, createdAt, updatedAt, deletedAt
- **Relacionamento**: 
  - Many-to-One com Product
  - Many-to-One com User

---

## 🔒 Segurança e Autenticação

### Autenticação JWT
- **Access Token**: Validade de 24 horas
- **Refresh Token**: Validade de 7 dias
- **Rotação de Tokens**: Tokens são rotacionados a cada refresh
- **Blacklist**: Tokens antigos são invalidados após rotação

### Google OAuth 2.0
- Integração completa com Google Sign-In
- Gerenciamento de estado OAuth
- Callback seguro com validação de estado
- Criação automática de usuários via Google

### Permissões
- **AllowAny**: Endpoints de login e callback OAuth
- **IsAuthenticated**: Todos os outros endpoints da API
- **Role-based**: Diferenciação entre ADMIN e COLLABORATOR

---

## 📊 Funcionalidades Especiais

### Soft Delete
Implementado em todos os modelos principais (User, Product, Supplier, MovementStock) através do campo `deletedAt`. Os registros não são removidos fisicamente do banco, preservando o histórico.

### Relatórios e Métricas
- **Contagem de Produtos por Categoria**: Agrupa produtos por categoria
- **Relatório de Lucro**: Calcula lucro total de saídas (vendas)
- **Relatório de Entradas e Saídas**: Totaliza movimentações por tipo

### Comandos Customizados
```powershell
# Criar usuários administradores padrão
python manage.py seed_admins
```

---

## 🎨 Interface Web

O sistema possui uma interface web completa e moderna:

- **Design Responsivo**: Funciona em desktop e dispositivos móveis
- **Dashboard Interativo**: Gráficos e métricas em tempo real
- **Formulários Validados**: Validação client-side e server-side
- **Feedback Visual**: Mensagens de sucesso/erro para todas as operações
- **Navegação Intuitiva**: Menu de navegação entre as páginas principais

---

## 🔄 Fluxo de Trabalho

1. **Autenticação**: Usuário faz login (email/senha ou Google)
2. **Token JWT**: Sistema gera e retorna access token
3. **Dashboard**: Usuário acessa dashboard com métricas
4. **Operações CRUD**: Gerencia produtos, categorias, fornecedores
5. **Movimentações**: Registra entradas e saídas de estoque
6. **Relatórios**: Visualiza métricas e análises

---

## 🛠️ Configurações Adicionais

### Banco de Dados MySQL (Opcional)

Para usar MySQL em vez de SQLite, configure em `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sistema-estoque',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_secret_key_aqui
DEBUG=True
GOOGLE_CLIENT_ID=seu_google_client_id
GOOGLE_CLIENT_SECRET=seu_google_client_secret
GOOGLE_CLIENT_SECRETS_FILE=caminho/arquivo.json
GOOGLE_REDIRECT_URI=http://127.0.0.1:8000/api/login/google/callback
```

---

## 📝 Notas de Desenvolvimento

- **CSRF**: Desabilitado para endpoints da API (usa JWT)
- **CORS**: Configure CORS para produção se necessário
- **Migrações**: Sempre execute `makemigrations` e `migrate` após mudanças em models
- **Testes**: Estrutura preparada para testes unitários em `tests.py`

---

## 🚧 Próximos Passos

- [ ] Implementar testes automatizados
- [ ] Adicionar paginação em listagens
- [ ] Implementar filtros e busca avançada
- [ ] Criar relatórios em PDF
- [ ] Adicionar notificações de estoque baixo
- [ ] Implementar histórico de alterações
- [ ] Deploy em produção

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos na disciplina de Programação Web da UFLA.

---

## 👥 Contribuindo

Este é um projeto acadêmico. Para sugestões ou melhorias, entre em contato com os desenvolvedores.
