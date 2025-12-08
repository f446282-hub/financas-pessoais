# 💰 Finanças Pessoais - Backend

API REST para gestão financeira pessoal, construída com FastAPI.

## 🚀 Quick Start

### Pré-requisitos

- Python 3.11+
- PostgreSQL 15+

---

## ⚠️ ATENÇÃO WINDOWS - LEIA PRIMEIRO! ⚠️

**Você está no Windows? Use os scripts automatizados OU siga os comandos abaixo:**

### 🚀 Método Rápido (Scripts Automatizados)

1. **Instalação completa:**
   ```cmd
   setup_windows.bat
   ```
   *(Este script cria o venv, instala dependências e configura tudo automaticamente)*

2. **Iniciar servidor:**
   ```cmd
   run.bat
   ```

### ⚠️ Problemas Comuns na Instalação

#### 🚨 Erro do Rust (pydantic-core)?

Se você vê: `Cargo, the Rust package manager, is not installed` e `ERRO: Falha ao instalar dependencias!`

**Solução DEFINITIVA (1 comando):**

```cmd
instalar_tudo_windows.bat
```

Este script resolve TUDO automaticamente! Veja: **[SOLUCAO_DEFINITIVA_RUST.md](SOLUCAO_DEFINITIVA_RUST.md)**

#### Problema com psycopg2-binary?

Se você receber erro ao instalar `psycopg2-binary`, veja:
- 📄 **[SOLUCAO_PSYCOPG2.md](SOLUCAO_PSYCOPG2.md)** - Soluções detalhadas
- 🔧 Execute: `install_psycopg2_windows.bat`

#### Solução Automatizada (Recomendado)

Para resolver TODOS os problemas automaticamente:

```cmd
instalar_tudo_windows.bat
```

Este script:
- ✅ Resolve problema do Rust (pydantic)
- ✅ Instala psycopg2-binary
- ✅ Instala todas as outras dependências
- ✅ Verifica se está tudo OK

#### Verificar se Está Tudo OK

Após a instalação, verifique se tudo está funcionando:

```cmd
verificar_instalacao.bat
```

Este script verifica todas as dependências e confirma se está tudo instalado corretamente.

---

### 📋 Método Manual - Passo a Passo Completo para Windows CMD

**IMPORTANTE:** Você já está no diretório `backend`, então NÃO execute `cd backend` novamente!

1. **Criar ambiente virtual** (se ainda não criou):
   ```cmd
   python -m venv venv
   ```

2. **Ativar ambiente virtual:**
   ```cmd
   venv\Scripts\activate.bat
   ```
   *(Você verá `(venv)` no início da linha do prompt quando ativado)*

3. **Instalar dependências:**
   ```cmd
   python -m pip install -r requirements.txt
   ```

4. **Copiar arquivo .env:**
   ```cmd
   copy .env.example .env
   ```

5. **Editar o arquivo .env** (com Notepad ou outro editor):
   ```cmd
   notepad .env
   ```
   *(Configure DATABASE_URL e SECRET_KEY)*

6. **Criar banco de dados PostgreSQL:**
   - Opção A: Via pgAdmin (recomendado)
   - Opção B: Via linha de comando (se psql estiver no PATH):
     ```cmd
     psql -U postgres -c "CREATE DATABASE financas_pessoais;"
     ```

7. **Rodar migrations** (com venv ativado):
   ```cmd
   python -m alembic upgrade head
   ```

8. **Iniciar servidor** (com venv ativado):
   ```cmd
   python -m uvicorn app.main:app --reload --port 8000
   ```

---

### Instalação Detalhada

**Windows (CMD/PowerShell):**

```cmd
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (CMD)
venv\Scripts\activate.bat
# ou (PowerShell)
venv\Scripts\Activate.ps1

# Instalar dependências
python -m pip install -r requirements.txt
```

**Linux/Mac:**

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Configuração

**Windows (CMD/PowerShell):**

```cmd
# Copiar arquivo de exemplo
copy .env.example .env

# Editar .env com suas configurações (use um editor de texto)
# - DATABASE_URL: URL do PostgreSQL
# - SECRET_KEY: Chave secreta para JWT (gere uma forte!)
```

**Linux/Mac:**

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas configurações
# - DATABASE_URL: URL do PostgreSQL
# - SECRET_KEY: Chave secreta para JWT (gere uma forte!)
```

### Banco de Dados

**Windows:**

```cmd
# Criar banco de dados usando psql (certifique-se que PostgreSQL está no PATH)
psql -U postgres -c "CREATE DATABASE financas_pessoais;"

# Ou use pgAdmin para criar o banco manualmente

# Rodar migrations (com venv ativado)
python -m alembic upgrade head
```

**Linux/Mac:**

```bash
# Criar banco de dados
createdb financas_pessoais

# Rodar migrations
alembic upgrade head
```

### Executar

**Windows (CMD/PowerShell):**

```cmd
# Certifique-se de que o ambiente virtual está ativado!

# Desenvolvimento
python -m uvicorn app.main:app --reload --port 8000

# Produção
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Linux/Mac:**

```bash
# Desenvolvimento
uvicorn app.main:app --reload --port 8000

# Produção
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 Documentação da API

Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🏗️ Estrutura

```
backend/
├── app/
│   ├── core/           # Configurações centrais
│   │   ├── config.py   # Settings
│   │   ├── database.py # Conexão DB
│   │   ├── security.py # JWT, hashing
│   │   └── dependencies.py # DI
│   ├── users/          # Domínio: Usuários
│   ├── accounts/       # Domínio: Contas e Cartões
│   ├── transactions/   # Domínio: Transações
│   ├── investments/    # Domínio: Investimentos
│   ├── indicators/     # Domínio: Indicadores
│   ├── integrations/   # Domínio: Integrações
│   ├── dashboard/      # Domínio: Dashboard
│   └── main.py         # Entry point
├── alembic/            # Migrations
├── requirements.txt
└── .env.example
```

## 🔐 Autenticação

A API usa JWT (JSON Web Tokens). Para acessar endpoints protegidos:

1. Registre-se: `POST /api/auth/register`
2. Faça login: `POST /api/auth/login`
3. Use o token no header: `Authorization: Bearer <token>`

## 📋 Endpoints Principais

### Auth
- `POST /api/auth/register` - Cadastro
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Dados do usuário logado

### Contas
- `GET /api/accounts` - Listar contas
- `POST /api/accounts` - Criar conta
- `GET /api/accounts/{id}` - Detalhe
- `PUT /api/accounts/{id}` - Atualizar
- `DELETE /api/accounts/{id}` - Remover

### Cartões
- `GET /api/credit-cards` - Listar cartões
- `POST /api/credit-cards` - Criar cartão

### Transações
- `GET /api/transactions` - Listar (com filtros)
- `POST /api/transactions` - Criar
- `GET /api/transactions/summary` - Resumo
- `GET /api/transactions/cash-flow` - Fluxo de caixa

### Dashboard
- `GET /api/dashboard` - Dados completos
- `GET /api/dashboard/summary` - Resumo
- `GET /api/dashboard/expenses-by-category` - Por categoria

### Investimentos
- `GET /api/investments/portfolios` - Carteiras
- `POST /api/investments/portfolios` - Nova carteira
- `POST /api/investments/portfolios/{id}/entries` - Aporte/Resgate

### Indicadores
- `GET /api/indicators` - Listar indicadores
- `GET /api/indicators/values` - Valores calculados

### Integrações
- `GET /api/integrations/banks/providers` - Bancos disponíveis
- `POST /api/integrations/banks/{provider}/connect` - Conectar
- `GET /api/integrations/whatsapp` - Config WhatsApp
- `PUT /api/integrations/whatsapp` - Atualizar WhatsApp

## 🧪 Testes

```bash
pytest
```

## 🔧 Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| DATABASE_URL | URL do PostgreSQL | - |
| SECRET_KEY | Chave para JWT | - |
| ALGORITHM | Algoritmo JWT | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Expiração do token | 1440 |
| CORS_ORIGINS | URLs permitidas | ["http://localhost:3000"] |
| DEBUG | Modo debug | false |
| ENVIRONMENT | Ambiente | development |

## 📄 Licença

Projeto privado - Todos os direitos reservados.
