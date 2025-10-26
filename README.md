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
</p>

---
## 👨‍💻 Equipe

- **Professor:** Raphael Winckler de Bettio
- **Alunos:** Augusto Inácio Silva Mariano e Érika Mara de Morais Machado

---

# 📌 Sobre o Projeto

##  🎯 1º CheckPoint
```
⚠️ Esta primeira etapa do projeto foca na definição da estrutura do banco de dados e modelagem do ambiente administrativo, preparando para futuras integrações, regras de negócio e funcionalidades mais complexas.
```

O projeto busca fornecer uma solução para gerenciamento de estoque utilizando conceitos de modelagem de dados. Cada produto está associado a categorias e fornecedores, e cada movimentação precisa ser registrada por um usuário responsável. O objetivo é estruturar a base de dados de forma organizada, garantindo que todas as informações necessárias para o controle de estoque sejam capturadas de maneira consistente.

Neste contexto, um banco de dados é utilizado para representar os produtos, categorias, fornecedores, usuários e movimentações. Cada tabela corresponde a uma entidade do sistema, e os relacionamentos entre elas permitem registrar operações de entrada e saída, associando cada ação a usuários e produtos específicos. 


--- 
##  🎯 Objetivos

- ✔ Permitir cadastro e gestão de produtos, categorias, fornecedores e usuários.
- ✔ Registrar movimentações de estoque (entrada/saída) associadas a produtos e usuários.
- ✔ Disponibilizar interface administrativa via Django Admin para administração e visualização gráfica dos dados.
  
--- 
## 🔧 Principais funcionalidades

- ✔ CRUD de Produtos, Categorias, Fornecedores, Usuários e Movimentações do Estoque, através do Django Admin.
- ✔ Migrations criadas para modelagem inicial do banco.

<p align="center">
  
![Modelagem BD](https://github.com/user-attachments/assets/fbfdab13-a605-4cee-8fb3-fe565b24cad6)

</p>

## ⚙️ Tecnologias utilizadas

- Python 3.13.2
- Django 5.2.7
- Banco de dados padrão: SQLite (arquivo `db.sqlite3`), com opção de configuração para MySQL em `sistema_estoque/settings.py`.

## 🚀 Como Usar?

### 📥 Instalação

Clone o repositório e acesse a pasta do projeto:

```bash
git clone git clone https://github.com/Gurinzada/sistema-estoque-programacao-web
cd "sistema-estoque-programacao-web"
```
## ▶️ Execução

1. Criar e ativar um virtualenv

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

2. Aplicar migrations:

```powershell
python manage.py migrate
```

4. Criar um superuser para acessar o admin:

```powershell
python manage.py createsuperuser
```

5. Rodar o servidor de desenvolvimento:

```powershell
python manage.py runserver
```

6. Acesse o admin em `http://127.0.0.1:8000/admin/`.

## 📂 Estrutura do Projeto

```bash
sistema-estoque-programacao-web/
├─ 📄 db.sqlite3
├─ 📄 manage.py
├─ 📁 estoque/
│  ├─ 📄 admin.py            # Registra modelos no Django Admin
│  ├─ 📄 apps.py             # Configuração da app 'estoque'
│  ├─ 📁 migrations/         # Migrations geradas pelo Django
│  │  ├─ 📄 0001_initial.py  # Cria tabelas iniciais (Category, User, Product, Supplier, MovementStock)
│  │  └─ 📄 0002_...py       # Alterações geradas posteriormente
│  ├─ 📄 models.py           # Modelos principais: User, Category, Product, MovementStock, Supplier
│  ├─ 📄 views.py            # Views (atualmente vazio)
│  ├─ 📄 admin.py            # Registro simples dos modelos no admin
│  └─ 📄 tests.py            # Arquivo para testes (atualmente vazio)
├─ 📁 sistema_estoque/
│  ├─ 📄 asgi.py
│  ├─ 📄 settings.py         # Configurações do projeto (INSTALLED_APPS, DATABASES, etc.)
│  ├─ 📄 urls.py             # Rotas principais (aponta para admin/)
│  └─ 📄 wsgi.py
```
