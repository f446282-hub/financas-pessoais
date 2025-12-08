"""
Router de Transações e Categorias.
Define endpoints CRUD para lançamentos financeiros.
"""

from typing import List, Optional
from uuid import UUID
from datetime import date
from fastapi import APIRouter, Query, status

from app.core.dependencies import CurrentUser, DatabaseSession
from app.transactions.models import TransactionType, TransactionStatus
from app.transactions.service import TransactionService, CategoryService
from app.transactions.schemas import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionListResponse,
    TransactionSummary,
    CashFlowResponse,
    CategoryCreate,
    CategoryResponse,
)


# Routers
transactions_router = APIRouter(prefix="/transactions", tags=["Transações"])
categories_router = APIRouter(prefix="/categories", tags=["Categorias"])


# ===========================================
# Endpoints de Transações
# ===========================================

@transactions_router.get(
    "",
    response_model=TransactionListResponse,
    summary="Listar transações",
    description="Lista transações do usuário com filtros opcionais.",
)
async def list_transactions(
    current_user: CurrentUser,
    db: DatabaseSession,
    start_date: Optional[date] = Query(None, description="Data inicial"),
    end_date: Optional[date] = Query(None, description="Data final"),
    type: Optional[TransactionType] = Query(None, description="Tipo: income ou expense"),
    status: Optional[TransactionStatus] = Query(None, description="Status"),
    account_id: Optional[UUID] = Query(None, description="Filtrar por conta"),
    credit_card_id: Optional[UUID] = Query(None, description="Filtrar por cartão"),
    category_id: Optional[UUID] = Query(None, description="Filtrar por categoria"),
    limit: int = Query(100, ge=1, le=500, description="Limite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginação"),
):
    """
    Lista transações com diversos filtros.
    
    Exemplos de uso:
    - Listar todas: GET /transactions
    - Por período: GET /transactions?start_date=2024-01-01&end_date=2024-01-31
    - Só receitas: GET /transactions?type=income
    - De uma conta: GET /transactions?account_id=uuid
    """
    service = TransactionService(db)
    
    transactions = service.get_all(
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
        tx_type=type,
        status=status,
        account_id=account_id,
        credit_card_id=credit_card_id,
        category_id=category_id,
        limit=limit,
        offset=offset,
    )
    
    # Calcular totais
    summary = service.get_summary(current_user.id, start_date, end_date)
    
    # Enriquecer transações
    enriched = [service.enrich_transaction(t) for t in transactions]
    
    return TransactionListResponse(
        transactions=[TransactionResponse(**t) for t in enriched],
        total=len(transactions),
        total_income=summary.total_income,
        total_expense=summary.total_expense,
        balance=summary.balance,
    )


@transactions_router.post(
    "",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar transação",
    description="Cria uma nova transação (receita ou despesa).",
)
async def create_transaction(
    data: TransactionCreate,
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """
    Cria um novo lançamento financeiro.
    
    A transação deve estar vinculada a uma **conta** OU um **cartão de crédito**.
    
    - Receitas: apenas em contas
    - Despesas: em contas ou cartões
    """
    service = TransactionService(db)
    transaction = service.create(current_user.id, data)
    
    enriched = service.enrich_transaction(transaction)
    return TransactionResponse(**enriched)


@transactions_router.get(
    "/summary",
    response_model=TransactionSummary,
    summary="Resumo de transações",
    description="Retorna resumo com totais e distribuição por categoria.",
)
async def get_summary(
    current_user: CurrentUser,
    db: DatabaseSession,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
):
    """
    Retorna resumo das transações no período.
    
    Inclui:
    - Total de receitas e despesas
    - Saldo (receitas - despesas)
    - Distribuição por categoria
    """
    service = TransactionService(db)
    return service.get_summary(current_user.id, start_date, end_date)


@transactions_router.get(
    "/cash-flow",
    response_model=CashFlowResponse,
    summary="Fluxo de caixa",
    description="Retorna fluxo de caixa diário do período.",
)
async def get_cash_flow(
    current_user: CurrentUser,
    db: DatabaseSession,
    start_date: date = Query(..., description="Data inicial"),
    end_date: date = Query(..., description="Data final"),
):
    """
    Retorna fluxo de caixa diário.
    
    Útil para gráficos de evolução de receitas e despesas.
    """
    service = TransactionService(db)
    result = service.get_cash_flow(current_user.id, start_date, end_date)
    return CashFlowResponse(**result)


@transactions_router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
    summary="Detalhe da transação",
    description="Retorna detalhes de uma transação específica.",
)
async def get_transaction(
    transaction_id: UUID,
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """Retorna os detalhes de uma transação específica."""
    service = TransactionService(db)
    transaction = service.get_by_id(transaction_id, current_user.id)
    
    enriched = service.enrich_transaction(transaction)
    return TransactionResponse(**enriched)


@transactions_router.put(
    "/{transaction_id}",
    response_model=TransactionResponse,
    summary="Atualizar transação",
    description="Atualiza uma transação existente.",
)
async def update_transaction(
    transaction_id: UUID,
    data: TransactionUpdate,
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """Atualiza os dados de uma transação."""
    service = TransactionService(db)
    transaction = service.update(transaction_id, current_user.id, data)
    
    enriched = service.enrich_transaction(transaction)
    return TransactionResponse(**enriched)


@transactions_router.delete(
    "/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir transação",
    description="Remove uma transação do sistema.",
)
async def delete_transaction(
    transaction_id: UUID,
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """Remove uma transação."""
    service = TransactionService(db)
    service.delete(transaction_id, current_user.id)


# ===========================================
# Endpoints de Categorias
# ===========================================

@categories_router.get(
    "",
    response_model=List[CategoryResponse],
    summary="Listar categorias",
    description="Lista categorias disponíveis (globais + personalizadas).",
)
async def list_categories(
    current_user: CurrentUser,
    db: DatabaseSession,
    type: Optional[TransactionType] = Query(None, description="Filtrar por tipo"),
):
    """
    Lista todas as categorias disponíveis para o usuário.
    
    Inclui categorias globais do sistema e personalizadas do usuário.
    """
    service = CategoryService(db)
    
    # Garantir que categorias padrão existem
    service.ensure_default_categories_exist()
    
    if type:
        categories = service.get_by_type(current_user.id, type)
    else:
        categories = service.get_all(current_user.id)
    
    return [CategoryResponse.model_validate(c) for c in categories]


@categories_router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar categoria",
    description="Cria uma nova categoria personalizada.",
)
async def create_category(
    data: CategoryCreate,
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """
    Cria uma nova categoria personalizada para o usuário.
    
    A categoria ficará disponível apenas para este usuário.
    """
    service = CategoryService(db)
    category = service.create(current_user.id, data)
    
    return CategoryResponse.model_validate(category)
