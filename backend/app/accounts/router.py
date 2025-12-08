"""
Router de Contas e Cartões de Crédito.
Define endpoints CRUD para gestão financeira.
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, status

from app.core.dependencies import CurrentUser, DatabaseSession
from app.accounts.service import AccountService, CreditCardService
from app.accounts.schemas import (
    AccountCreate,
    AccountUpdate,
    AccountResponse,
    AccountListResponse,
    CreditCardCreate,
    CreditCardUpdate,
    CreditCardResponse,
    CreditCardListResponse,
)


# Routers
accounts_router = APIRouter(prefix="/accounts", tags=["Contas"])
credit_cards_router = APIRouter(prefix="/credit-cards", tags=["Cartões de Crédito"])


# ===========================================
# Endpoints de Contas
# ===========================================

@accounts_router.get(
    "",
    response_model=AccountListResponse,
    summary="Listar contas",
    description="Lista todas as contas do usuário.",
)
async def list_accounts(
    current_user: CurrentUser,
    db: DatabaseSession,
    include_inactive: bool = False,
):
    """
    Lista todas as contas do usuário autenticado.
    
    - **include_inactive**: Se True, inclui contas inativas
    """
    service = AccountService(db)
    accounts = service.get_all(current_user.id, include_inactive)
    total_balance = service.get_total_balance(current_user.id)
    
    return AccountListResponse(
        accounts=[AccountResponse.model_validate(a) for a in accounts],
        total=len(accounts),
        total_balance=total_balance,
    )


@accounts_router.post(
    "",
    response_model=AccountResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar conta",
    description="Cria uma nova conta para o usuário.",
)
async def create_account(
    data: AccountCreate,
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """
    Cria uma nova conta bancária/financeira.
    
    Tipos disponíveis:
    - **checking**: Conta corrente
    - **savings**: Poupança
    - **wallet**: Carteira
    - **investment**: Conta investimento
    - **other**: Outros
    """
    service = AccountService(db)
    account = service.create(current_user.id, data)
    
    return AccountResponse.model_validate(account)


@accounts_router.get(
    "/{account_id}",
    response_model=AccountResponse,
    summary="Detalhe da conta",
    description="Retorna detalhes de uma conta específica.",
)
async def get_account(
    account_id: UUID,
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """Retorna os detalhes de uma conta específica."""
    service = AccountService(db)
    account = service.get_by_id(account_id, current_user.id)
    
    return AccountResponse.model_validate(account)


@accounts_router.put(
    "/{account_id}",
    response_model=AccountResponse,
    summary="Atualizar conta",
    description="Atualiza uma conta existente.",
)
async def update_account(
    account_id: UUID,
    data: AccountUpdate,
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """Atualiza os dados de uma conta."""
    service = AccountService(db)
    account = service.update(account_id, current_user.id, data)
    
    return AccountResponse.model_validate(account)


@accounts_router.delete(
    "/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir conta",
    description="Remove uma conta do sistema.",
)
async def delete_account(
    account_id: UUID,
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """
    Remove uma conta.
    
    **Atenção**: Todas as transações vinculadas serão excluídas.
    """
    service = AccountService(db)
    service.delete(account_id, current_user.id)


# ===========================================
# Endpoints de Cartões de Crédito
# ===========================================

@credit_cards_router.get(
    "",
    response_model=CreditCardListResponse,
    summary="Listar cartões",
    description="Lista todos os cartões de crédito do usuário.",
)
async def list_credit_cards(
    current_user: CurrentUser,
    db: DatabaseSession,
    include_inactive: bool = False,
):
    """
    Lista todos os cartões do usuário autenticado.
    
    - **include_inactive**: Se True, inclui cartões inativos
    """
    service = CreditCardService(db)
    cards = service.get_all(current_user.id, include_inactive)
    total_limit = service.get_total_limit(current_user.id)
    
    # Enriquecer com dados calculados
    card_responses = []
    for card in cards:
        response = CreditCardResponse.model_validate(card)
        response.current_invoice = service.get_current_invoice(card.id, current_user.id)
        response.available_limit = card.limit - (response.current_invoice or 0)
        card_responses.append(response)
    
    return CreditCardListResponse(
        cards=card_responses,
        total=len(cards),
        total_limit=total_limit,
    )


@credit_cards_router.post(
    "",
    response_model=CreditCardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar cartão",
    description="Cria um novo cartão de crédito.",
)
async def create_credit_card(
    data: CreditCardCreate,
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """
    Cria um novo cartão de crédito.
    
    - **closing_day**: Dia do mês em que a fatura fecha (1-31)
    - **due_day**: Dia do mês em que a fatura vence (1-31)
    """
    service = CreditCardService(db)
    card = service.create(current_user.id, data)
    
    return CreditCardResponse.model_validate(card)


@credit_cards_router.get(
    "/{card_id}",
    response_model=CreditCardResponse,
    summary="Detalhe do cartão",
    description="Retorna detalhes de um cartão específico.",
)
async def get_credit_card(
    card_id: UUID,
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """Retorna os detalhes de um cartão específico."""
    service = CreditCardService(db)
    card = service.get_by_id(card_id, current_user.id)
    
    response = CreditCardResponse.model_validate(card)
    response.current_invoice = service.get_current_invoice(card.id, current_user.id)
    response.available_limit = card.limit - (response.current_invoice or 0)
    
    return response


@credit_cards_router.put(
    "/{card_id}",
    response_model=CreditCardResponse,
    summary="Atualizar cartão",
    description="Atualiza um cartão existente.",
)
async def update_credit_card(
    card_id: UUID,
    data: CreditCardUpdate,
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """Atualiza os dados de um cartão."""
    service = CreditCardService(db)
    card = service.update(card_id, current_user.id, data)
    
    return CreditCardResponse.model_validate(card)


@credit_cards_router.delete(
    "/{card_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir cartão",
    description="Remove um cartão do sistema.",
)
async def delete_credit_card(
    card_id: UUID,
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """
    Remove um cartão.
    
    **Atenção**: Todas as transações vinculadas serão excluídas.
    """
    service = CreditCardService(db)
    service.delete(card_id, current_user.id)
