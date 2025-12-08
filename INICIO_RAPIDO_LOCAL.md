# ⚡ Início Rápido - Rodar Localmente (SQLite)

## 🎯 Objetivo

Rodar o sistema completo **localmente** sem precisar instalar PostgreSQL!

## 🚀 Método Mais Rápido (1 Comando)

Execute na raiz do projeto:

```cmd
rodar_local.bat
```

Isso vai:
- ✅ Configurar SQLite automaticamente
- ✅ Iniciar backend
- ✅ Iniciar frontend
- ✅ Abrir navegador

**Pronto!** Acesse: http://localhost:3000

## 📋 Método Manual (Passo a Passo)

### 1. Backend (SQLite)

```cmd
cd backend

REM Criar .env com SQLite
copy .env.local.example .env
notepad .env

REM Ativar venv
venv\Scripts\activate.bat

REM Executar migrations (cria o banco SQLite)
python -m alembic upgrade head

REM Iniciar servidor
python -m uvicorn app.main:app --reload --port 8000
```

### 2. Frontend (Outro Terminal)

```cmd
cd frontend

REM Instalar (primeira vez)
setup_windows.bat

REM Iniciar servidor
run_windows.bat
```

## ⚙️ Configuração do .env (Backend)

Edite `backend/.env`:

```env
DATABASE_URL=sqlite:///./financas_pessoais.db
SECRET_KEY=minha-chave-local-123
DEBUG=true
ENVIRONMENT=development
```

## 📁 Onde Fica o Banco?

O SQLite cria um arquivo em:
```
backend/financas_pessoais.db
```

Este arquivo contém todos os seus dados locais.

## 🔄 Migrar para PostgreSQL Depois

Quando quiser usar PostgreSQL:

1. Configure `.env` com:
   ```env
   DATABASE_URL=postgresql://usuario:senha@localhost:5432/financas_pessoais
   ```

2. Crie o banco no PostgreSQL

3. Execute migrations novamente

## ✅ Checklist

- [ ] Backend rodando (http://localhost:8000/docs)
- [ ] Frontend rodando (http://localhost:3000)
- [ ] Banco SQLite criado (`backend/financas_pessoais.db`)

## 🆘 Problemas?

- **Migrations não rodam?** Certifique-se de que o ambiente virtual está ativado
- **Erro de conexão?** Verifique o `DATABASE_URL` no `.env`
- **Frontend não conecta?** Verifique se o backend está rodando

## 📚 Documentação Completa

Veja: `backend/GUIA_RODAR_LOCAL.md` para detalhes completos.

---

**Dica:** Use SQLite para desenvolvimento, PostgreSQL para produção! 🚀

