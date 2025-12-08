# 🏠 Guia: Rodar Localmente com SQLite (Sem PostgreSQL)

Este guia mostra como rodar o sistema **localmente** usando **SQLite** ao invés de PostgreSQL. Ideal para desenvolvimento e testes rápidos!

## 🎯 Por Que SQLite?

- ✅ **Não precisa instalar PostgreSQL**
- ✅ **Rápido para começar**
- ✅ **Perfeito para desenvolvimento**
- ✅ **Funciona em qualquer lugar**
- ✅ **Zero configuração**

## 🚀 Início Rápido

### 1. Configurar Backend para SQLite

Crie ou edite o arquivo `.env` na pasta `backend/`:

```env
# Usar SQLite (arquivo local)
DATABASE_URL=sqlite:///./financas_pessoais.db

# Ou usar caminho absoluto:
# DATABASE_URL=sqlite:///D:/financas-pessoais/backend/financas_pessoais.db

# Outras configurações
SECRET_KEY=sua-chave-secreta-local
DEBUG=true
ENVIRONMENT=development
```

### 2. Rodar Migrations

```cmd
cd backend
venv\Scripts\activate.bat
python -m alembic upgrade head
```

### 3. Iniciar Backend

```cmd
python -m uvicorn app.main:app --reload --port 8000
```

### 4. Iniciar Frontend

Em outro terminal:

```cmd
cd frontend
npm run dev
```

Pronto! Acesse: http://localhost:3000

## 📋 Passo a Passo Completo

### Backend

1. **Criar arquivo .env com SQLite:**

   ```cmd
   cd backend
   copy .env.example .env
   notepad .env
   ```

   Edite e configure:
   ```env
   DATABASE_URL=sqlite:///./financas_pessoais.db
   SECRET_KEY=minha-chave-secreta-local-123
   DEBUG=true
   ```

2. **Instalar dependências (se ainda não fez):**

   ```cmd
   venv\Scripts\activate.bat
   instalar_tudo_windows.bat
   ```

3. **Executar migrations:**

   ```cmd
   python -m alembic upgrade head
   ```

   Isso criará o arquivo `financas_pessoais.db` automaticamente.

4. **Iniciar servidor:**

   ```cmd
   python -m uvicorn app.main:app --reload --port 8000
   ```

### Frontend

1. **Instalar dependências:**

   ```cmd
   cd frontend
   setup_windows.bat
   ```

2. **Iniciar servidor:**

   ```cmd
   run_windows.bat
   ```

   Ou manualmente:
   ```cmd
   npm run dev
   ```

## 🎁 Script Automatizado

Criei um script que faz tudo automaticamente! Execute na raiz do projeto:

```cmd
rodar_local.bat
```

Este script:
- ✅ Configura SQLite automaticamente
- ✅ Inicia backend (porta 8000)
- ✅ Inicia frontend (porta 3000)
- ✅ Abre navegador automaticamente

## 📁 Onde Fica o Banco de Dados?

O SQLite cria um arquivo `.db` na pasta `backend/`:

```
backend/
└── financas_pessoais.db  ← Banco de dados SQLite
```

**Importante:** Este arquivo contém todos os seus dados. Faça backup se necessário!

## 🔄 Migrar de SQLite para PostgreSQL (Depois)

Quando quiser usar PostgreSQL em produção:

1. **Configure o .env com PostgreSQL:**

   ```env
   DATABASE_URL=postgresql://usuario:senha@localhost:5432/financas_pessoais
   ```

2. **Crie o banco no PostgreSQL:**

   ```sql
   CREATE DATABASE financas_pessoais;
   ```

3. **Rode migrations novamente:**

   ```cmd
   python -m alembic upgrade head
   ```

## ⚙️ Diferenças: SQLite vs PostgreSQL

| Característica | SQLite | PostgreSQL |
|----------------|--------|------------|
| Instalação | Já vem com Python | Precisa instalar |
| Performance | Bom para pequeno/médio | Excelente |
| Escalabilidade | Limitado | Ilimitada |
| Multiusuário | Limitado | Suporta |
| Uso recomendado | Desenvolvimento/Testes | Produção |

## 🆘 Problemas Comuns

### Erro: "No such table"

**Solução:** Execute as migrations:
```cmd
python -m alembic upgrade head
```

### Erro: "Database is locked"

**Solução:** Certifique-se de que não há outro processo usando o banco. Feche todas as conexões.

### Quero limpar os dados

**Solução:** Delete o arquivo `.db` e rode migrations novamente:
```cmd
del financas_pessoais.db
python -m alembic upgrade head
```

## ✅ Checklist

- [ ] Arquivo `.env` configurado com SQLite
- [ ] Dependências instaladas
- [ ] Migrations executadas
- [ ] Backend rodando na porta 8000
- [ ] Frontend rodando na porta 3000
- [ ] Acessando http://localhost:3000

## 🎉 Pronto!

Agora você pode desenvolver e testar localmente sem precisar do PostgreSQL!

---

**Dica:** Use SQLite para desenvolvimento e PostgreSQL para produção! 🚀

