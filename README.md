# 💰 Finanças Pessoais

Sistema completo de gestão financeira pessoal com backend FastAPI e frontend Next.js.

## 🚀 Quick Start

### Desenvolvimento Local (SQLite)

Execute um comando e tudo inicia automaticamente:

```cmd
Iniciar_Sistema_MELHORADO.bat
```

Ou use o script na raiz:

```cmd
rodar_local.bat
```

Isso vai:
- ✅ Configurar SQLite automaticamente
- ✅ Iniciar Backend (porta 8000)
- ✅ Iniciar Frontend (porta 3000)
- ✅ Abrir navegador

## 📋 Pré-requisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (opcional - pode usar SQLite local)

## 🏗️ Estrutura do Projeto

```
financas-pessoais/
├── backend/          # API FastAPI
│   ├── app/
│   ├── alembic/      # Migrations
│   └── venv/         # Ambiente virtual
├── frontend/         # Interface Next.js
│   ├── src/
│   └── node_modules/
└── Scripts/          # Scripts de automação
```

## 🔧 Instalação

### Backend

```cmd
cd backend
setup_windows.bat
# ou manualmente:
python -m venv venv
venv\Scripts\activate.bat
instalar_tudo_windows.bat
```

### Frontend

```cmd
cd frontend
setup_windows.bat
# ou manualmente:
npm install
```

## 🚀 Executar

### Método Automático

```cmd
Iniciar_Sistema_MELHORADO.bat
```

### Método Manual

**Backend:**
```cmd
cd backend
venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```cmd
cd frontend
npm run dev
```

Acesse: http://localhost:3000

## 📚 Documentação

- **Desenvolvimento Local:** `GUIA_RODAR_LOCAL.md`
- **Problemas Comuns:** `backend/SOLUCAO_RAPIDA.md`
- **GitHub:** `GUIA_GITHUB.md`
- **Build Executável:** `GUIA_BUILD.md`

## 🛠️ Scripts Disponíveis

### Verificação
- `verificar_requisitos.bat` - Verifica se tudo está instalado

### Iniciar Sistema
- `Iniciar_Sistema_MELHORADO.bat` - Inicia tudo automaticamente
- `rodar_local.bat` - Inicia com SQLite local

### Backend
- `backend/setup_windows.bat` - Instala backend
- `backend/run.bat` - Inicia apenas backend

### Frontend
- `frontend/setup_windows.bat` - Instala frontend
- `frontend/run_windows.bat` - Inicia apenas frontend

### GitHub
- `enviar_github.bat` - Envia projeto para GitHub

## 🔐 Configuração

### Backend (.env)

```env
DATABASE_URL=sqlite:///./financas_pessoais.db
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=true
ENVIRONMENT=development
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=Finanças Pessoais
```

## 📊 Tecnologias

### Backend
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL / SQLite

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- Recharts

## 📄 Licença

Projeto privado - Todos os direitos reservados.

---

**Desenvolvido para facilitar a gestão financeira pessoal** 💰
