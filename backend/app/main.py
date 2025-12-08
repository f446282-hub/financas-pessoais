"""
Finanças Pessoais - API REST

Plataforma de gestão financeira pessoal.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

# Import de routers
from app.users.router import auth_router, users_router
from app.accounts.router import accounts_router, credit_cards_router
from app.transactions.router import transactions_router, categories_router
from app.investments.service import investments_router
from app.indicators import indicators_router
from app.integrations import integrations_router
from app.dashboard import dashboard_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciador de ciclo de vida da aplicação."""
    print(f"🚀 Iniciando {settings.app_name} v{settings.app_version}")
    print(f"📍 Ambiente: {settings.environment}")
    yield
    print("👋 Encerrando aplicação...")


# Criar aplicação FastAPI
app = FastAPI(
    title=settings.app_name,
    description="""
## 💰 Finanças Pessoais API

Plataforma completa de gestão financeira pessoal.

### Recursos

- 🔐 **Autenticação**: Registro, login e gestão de perfil
- 💳 **Contas**: Gestão de contas bancárias e carteiras
- 💳 **Cartões**: Gestão de cartões de crédito
- 📝 **Transações**: Controle de receitas e despesas
- 📈 **Investimentos**: Acompanhamento de carteiras
- 📊 **Indicadores**: Métricas financeiras
- 🔗 **Integrações**: Conexão com bancos e WhatsApp
- 📉 **Dashboard**: Visualização consolidada

### Autenticação

Use o endpoint `/api/auth/login` para obter um token JWT.
Inclua o token no header: `Authorization: Bearer <token>`
    """,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["Health"])
async def health_check():
    """Verifica se a API está funcionando."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


# Registrar Routers
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(accounts_router, prefix="/api")
app.include_router(credit_cards_router, prefix="/api")
app.include_router(transactions_router, prefix="/api")
app.include_router(categories_router, prefix="/api")
app.include_router(investments_router, prefix="/api")
app.include_router(indicators_router, prefix="/api")
app.include_router(integrations_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")


@app.get("/", tags=["Root"])
async def root():
    """Redireciona para a documentação."""
    return {
        "message": f"Bem-vindo ao {settings.app_name}!",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/health",
    }
