<div align="center">

<img src="https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white"/>
<img src="https://img.shields.io/badge/JWT-Auth-orange?style=for-the-badge&logo=jsonwebtokens&logoColor=white"/>
<img src="https://img.shields.io/badge/Alembic-Migrations-blue?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Deploy-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white"/>
<img src="https://img.shields.io/badge/DIO-Desafio_Final-C624C1?style=for-the-badge"/>

# 🏦 Bank API

**API Bancária Assíncrona com FastAPI — Desafio Final DIO**

*Autenticação JWT · Contas Bancárias · Transações · PostgreSQL · Deploy no Render*

[🚀 Demo no Render](#deploy) · [📖 Endpoints](#endpoints) · [🔐 Segurança](#segurança) · [⚡ Quick Start](#quick-start)

</div>

---

## 📋 Sobre o Projeto

API bancária **100% assíncrona** desenvolvida como desafio final do bootcamp **Jornada para o Futuro** da [DIO](https://dio.me). Aplica todos os conceitos do curso: FastAPI assíncrono, autenticação JWT, banco de dados relacional com SQLAlchemy async, migrations com Alembic e deploy em produção no Render com PostgreSQL.

### ✨ Funcionalidades

| Feature | Descrição |
|---------|-----------|
| 🔐 **Autenticação JWT** | Register, login e proteção de rotas com Bearer token |
| 🏦 **Contas Bancárias** | Criação automática com número único de 10 dígitos |
| 💰 **Depósito** | Crédito em conta com histórico de transação |
| 💸 **Saque** | Débito com validação de saldo suficiente |
| 🔄 **Transferência** | Entre contas com validação de saldo e conta destino |
| 📊 **Histórico** | Extrato completo de transações por conta |
| 🗄️ **Migrations** | Alembic para versionamento do schema do banco |
| 🚀 **Deploy** | Render com PostgreSQL free tier + `render.yaml` |

---

## 🏗️ Arquitetura

```
bank-api/
├── main.py                  ← Entry point · lifespan · CORS · health check
├── config.py                ← Pydantic Settings · SQLite (dev) / PostgreSQL (prod)
├── database.py              ← Engine async · pool sizing · get_db()
├── models.py                ← User · Account · Transaction (SQLAlchemy 2.0)
├── schemas.py               ← Pydantic v2 · validação de entrada/saída
├── dependencies.py          ← get_current_user · JWT Bearer
├── services/
│   ├── auth_service.py      ← bcrypt · JWT · timing-safe login
│   └── account_service.py   ← CRUD · regras de negócio · transações
├── routers/
│   ├── auth.py              ← /auth/register · /auth/login · /auth/me
│   └── accounts.py          ← /accounts/* · depósito · saque · transferência
├── alembic/
│   └── versions/
│       └── 0001_initial.py  ← migration: users · accounts · transactions
├── Procfile                 ← alembic upgrade head && uvicorn
├── render.yaml              ← blueprint: Web Service + PostgreSQL free tier
├── SECURITY_REPORT.md       ← checklist OWASP
└── requirements.txt
```

### Modelo de dados

```
User ──────────── Account ──────────── Transaction
 id               id                   id
 username         number (unique)      type (deposit/withdrawal/transfer)
 email            balance              amount
 hashed_password  is_active            description
 is_active        user_id (FK)         account_id (FK)
 created_at       created_at           target_account_id (FK, nullable)
                                       created_at
```

---

## ⚡ Quick Start

### Pré-requisitos

- Python 3.11+
- pip

### Instalação local

```bash
# Clone o repositório
git clone https://github.com/taissocout/bank-api.git
cd bank-api

# Configure as variáveis de ambiente
cp .env.example .env

# Instale as dependências
pip install -r requirements.txt

# Execute as migrations
alembic upgrade head

# Inicie o servidor
uvicorn main:app --reload --port 8003
```

Acesse a documentação interativa: **http://localhost:8003/docs**

---

## 📖 Endpoints

### 🔐 Auth

| Método | Rota | Descrição | Auth |
|--------|------|-----------|:----:|
| `POST` | `/auth/register` | Registra novo usuário | ❌ |
| `POST` | `/auth/login` | Login e retorna JWT | ❌ |
| `GET`  | `/auth/me` | Dados do usuário logado | ✅ |

### 🏦 Accounts

| Método | Rota | Descrição | Auth |
|--------|------|-----------|:----:|
| `POST` | `/accounts/` | Cria nova conta bancária | ✅ |
| `GET`  | `/accounts/` | Lista todas as contas do usuário | ✅ |
| `GET`  | `/accounts/{id}` | Detalhes de uma conta | ✅ |
| `POST` | `/accounts/{id}/deposit` | Realiza depósito | ✅ |
| `POST` | `/accounts/{id}/withdraw` | Realiza saque | ✅ |
| `POST` | `/accounts/{id}/transfer` | Realiza transferência | ✅ |
| `GET`  | `/accounts/{id}/history` | Extrato de transações | ✅ |

### ❤️ Health

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET`  | `/` | Status da API |
| `GET`  | `/health` | Health check (monitoramento Render) |

---

## 🧪 Exemplos de uso

### 1. Registrar usuário

```bash
curl -X POST http://localhost:8003/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "taissocout", "email": "taissocout@email.com", "password": "senha123"}'
```

### 2. Fazer login e guardar o token

```bash
TOKEN=$(curl -s -X POST http://localhost:8003/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "taissocout", "password": "senha123"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
```

### 3. Criar conta bancária

```bash
curl -X POST http://localhost:8003/accounts/ \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Depositar R$ 500,00

```bash
curl -X POST http://localhost:8003/accounts/1/deposit \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": 500.00, "description": "Depósito inicial"}'
```

### 5. Tentar sacar mais do que tem (deve retornar 422)

```bash
curl -X POST http://localhost:8003/accounts/1/withdraw \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": 9999.00}'
# {"detail": "Saldo insuficiente. Saldo: 500.00, Solicitado: 9999.00"}
```

### 6. Ver histórico de transações

```bash
curl http://localhost:8003/accounts/1/history \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🗄️ Banco de dados

| Ambiente | Driver | URL |
|----------|--------|-----|
| Desenvolvimento | `aiosqlite` | `sqlite+aiosqlite:///./bank.db` |
| Produção (Render) | `asyncpg` | `postgresql+asyncpg://...` (injetada automaticamente) |

A detecção é automática via `DATABASE_URL` — nenhuma alteração de código necessária entre ambientes.

### Migrations com Alembic

```bash
# Aplicar todas as migrations
alembic upgrade head

# Criar nova migration
alembic revision --autogenerate -m "descricao da alteracao"

# Reverter última migration
alembic downgrade -1

# Ver histórico
alembic history
```

---

## 🚀 Deploy

### Render (produção)

O projeto inclui `render.yaml` com blueprint completo:

```yaml
# Web Service + PostgreSQL free tier configurados automaticamente
services:
  - type: web
    name: bank-api
    startCommand: alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Passos:**
1. [render.com](https://render.com) → **New Web Service**
2. Conectar repositório `taissocout/bank-api`
3. Root Directory: `/` (raiz do repo)
4. Render detecta o `render.yaml` automaticamente
5. Adicionar PostgreSQL free tier → `DATABASE_URL` injetada automaticamente
6. Definir `APP_ENV=production`

### Deploy via API (curl)

```bash
export RENDER_API_KEY="sua_api_key"
bash deploy_render.sh
```

---

## 🔐 Segurança

Implementação baseada no **OWASP Top 10**:

| Controle | OWASP | Implementação |
|----------|:-----:|---------------|
| Senhas com bcrypt (cost=12) | A02 | `passlib[bcrypt]` |
| ORM — zero raw SQL | A03 | `SQLAlchemy async` |
| JWT com expiração configurável | A07 | `python-jose` |
| Login timing-safe | A07 | `verify_password` sempre executado |
| Stack trace nunca ao cliente | A09 | Global exception handler |
| Docs/OpenAPI off em produção | A05 | `docs_url=None` se `APP_ENV=production` |
| CORS explícito (sem `*`) | A05 | `allowed_origins` via env var |
| `SECRET_KEY` gerada automaticamente | A02 | `render.yaml` → `generateValue: true` |
| `.env` no `.gitignore` | A02 | Nunca commitado |
| Saldo nunca negativo | Negócio | Validação no service layer |

---

## ⚙️ Variáveis de ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `DATABASE_URL` | `sqlite+aiosqlite:///./bank.db` | Connection string do banco |
| `APP_ENV` | `development` | `development` ou `production` |
| `SECRET_KEY` | *(obrigatório em prod)* | Chave para assinar JWT |
| `ALGORITHM` | `HS256` | Algoritmo JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Expiração do token em minutos |
| `ALLOWED_ORIGINS` | `http://localhost:3000` | Origens CORS permitidas |

---

## 📚 Módulos do Bootcamp cobertos

| # | Módulo | Status |
|---|--------|:------:|
| 1 | Introdução ao Desenvolvimento Web | ✅ |
| 2 | Introdução ao FastAPI para APIs RESTful Assíncronas | ✅ |
| 3 | Primeiros passos com FastAPI | ✅ |
| 4 | Explorando Banco de Dados Relacionais com Python DB API | ✅ |
| 5 | Manipulação de Dados com FastAPI Assíncrono | ✅ |
| 6 | Autenticação e Autorização em FastAPI | ✅ |
| 7 | Testando APIs RESTful Assíncronas em FastAPI | ✅ |
| 8 | Deploy de uma API FastAPI Assíncrona | ✅ |
| 9 | **Desafio: Criando sua API Bancária Assíncrona** | ✅ |

---

## 🛠️ Stack completa

| Categoria | Tecnologia | Versão |
|-----------|-----------|--------|
| Framework | FastAPI | 0.111.0 |
| Servidor | Uvicorn | 0.29.0 |
| ORM | SQLAlchemy async | 2.0.36 |
| Driver PostgreSQL | asyncpg | 0.30.0 |
| Driver SQLite | aiosqlite | 0.20.0 |
| Validação | Pydantic v2 | 2.7.1 |
| Configuração | pydantic-settings | 2.2.1 |
| JWT | python-jose | 3.3.0 |
| Hash | passlib[bcrypt] | 1.7.4 |
| Migrations | Alembic | 1.13.1 |
| Deploy | Render | free tier |

---

<div align="center">

Desenvolvido durante o bootcamp **Jornada para o Futuro** da [DIO](https://dio.me) · 2026

[![GitHub](https://img.shields.io/badge/GitHub-taissocout-181717?style=flat&logo=github)](https://github.com/taissocout/bank-api)

</div>
