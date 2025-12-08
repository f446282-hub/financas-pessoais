"""
Schemas Pydantic para Transações e Categorias.
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, model_validator

from app.transactions.models import TransactionType, TransactionStatus


# ===========================================
# Category Schemas
# ===========================================

class CategoryBase(BaseModel):
    """Schema base de categoria."""
    
    name: str = Field(..., min_length=1, max_length=100, description="Nome da categoria")
    type: TransactionType = Field(..., description="Tipo: income ou expense")
    icon: Optional[str] = Field(None, max_length=50, description="Nome do ícone")
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$", description="Cor em hex")


class CategoryCreate(CategoryBase):
    """Schema para criação de categoria."""
    pass


class CategoryResponse(BaseModel):
    """Schema de resposta de categoria."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: Optional[UUID] = None
    name: str
    type: TransactionType
    icon: Optional[str] = None
    color: Optional[str] = None
    is_active: bool


# ===========================================
# Transaction Schemas
# ===========================================

class TransactionBase(BaseModel):
    """Schema base de transação."""
    
    type: TransactionType = Field(..., description="Tipo: income ou expense")
    description: str = Field(..., min_length=1, max_length=255, description="Descrição")
    amount: Decimal = Field(..., gt=0, description="Valor (sempre positivo)")
    date: date = Field(..., description="Data do lançamento")
    status: TransactionStatus = Field(
        default=TransactionStatus.PAID,
        description="Status: pending, paid, cancelled"
    )
    is_recurring: bool = Field(default=False, description="É recorrente?")
    notes: Optional[str] = Field(None, description="Observações")


class TransactionCreate(TransactionBase):
    """Schema para criação de transação."""
    
    account_id: Optional[UUID] = Field(None, description="ID da conta (se origem for conta)")
    credit_card_id: Optional[UUID] = Field(None, description="ID do cartão (se origem for cartão)")
    category_id: Optional[UUID] = Field(None, description="ID da categoria")
    
    @model_validator(mode="after")
    def validate_source(self):
        """Valida que transação tem conta OU cartão, não ambos."""
        if self.account_id and self.credit_card_id:
            raise ValueError("Transação não pode ter conta E cartão ao mesmo tempo")
        if not self.account_id and not self.credit_card_id:
            raise ValueError("Transação deve ter uma conta OU um cartão")
        # Cartão só aceita despesas
        if self.credit_card_id and self.type == TransactionType.INCOME:
            raise ValueError("Cartão de crédito não aceita receitas")
        return self


class TransactionUpdate(BaseModel):
    """Schema para atualização de transação."""
    
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    amount: Optional[Decimal] = Field(None, gt=0)
    date: Optional[date] = None
    status: Optional[TransactionStatus] = None
    category_id: Optional[UUID] = None
    notes: Optional[str] = None


class TransactionResponse(BaseModel):
    """Schema de resposta de transação."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    account_id: Optional[UUID] = None
    credit_card_id: Optional[UUID] = None
    category_id: Optional[UUID] = None
    type: TransactionType
    description: str
    amount: Decimal
    date: date
    status: TransactionStatus
    is_recurring: bool
    recurring_id: Optional[UUID] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Campos enriquecidos (opcionais, preenchidos pelo service)
    account_name: Optional[str] = None
    credit_card_name: Optional[str] = None
    category_name: Optional[str] = None
    category_color: Optional[str] = None


class TransactionFilters(BaseModel):
    """Filtros para listagem de transações."""
    
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    type: Optional[TransactionType] = None
    status: Optional[TransactionStatus] = None
    account_id: Optional[UUID] = None
    credit_card_id: Optional[UUID] = None
    category_id: Optional[UUID] = None


class TransactionListResponse(BaseModel):
    """Schema de resposta para lista de transações."""
    
    transactions: List[TransactionResponse]
    total: int
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal


class TransactionSummary(BaseModel):
    """Resumo de transações por período."""
    
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal
    transaction_count: int
    
    # Por categoria
    expenses_by_category: List[dict] = []
    income_by_category: List[dict] = []


# ===========================================
# Cash Flow Schemas
# ===========================================

class DailyCashFlow(BaseModel):
    """Fluxo de caixa diário."""
    
    date: date
    income: Decimal
    expense: Decimal
    balance: Decimal


class CashFlowResponse(BaseModel):
    """Resposta do fluxo de caixa."""
    
    period_start: date
    period_end: date
    daily_flow: List[DailyCashFlow]
    total_income: Decimal
    total_expense: Decimal
    net_flow: Decimal
