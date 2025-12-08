"""
Schemas Pydantic para Contas e Cartões de Crédito.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, field_validator

from app.accounts.models import AccountType


# ===========================================
# Account Schemas
# ===========================================

class AccountBase(BaseModel):
    """Schema base de conta."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Nome da conta")
    type: AccountType = Field(default=AccountType.CHECKING, description="Tipo da conta")
    institution: Optional[str] = Field(None, max_length=255, description="Banco/Instituição")
    initial_balance: Decimal = Field(default=Decimal("0.00"), description="Saldo inicial")
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$", description="Cor em hex")


class AccountCreate(AccountBase):
    """Schema para criação de conta."""
    pass


class AccountUpdate(BaseModel):
    """Schema para atualização de conta."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[AccountType] = None
    institution: Optional[str] = Field(None, max_length=255)
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    is_active: Optional[bool] = None


class AccountResponse(BaseModel):
    """Schema de resposta de conta."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    name: str
    type: AccountType
    institution: Optional[str] = None
    initial_balance: Decimal
    current_balance: Decimal
    color: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class AccountSummary(BaseModel):
    """Schema resumido de conta (para listagens)."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    type: AccountType
    institution: Optional[str] = None
    current_balance: Decimal
    color: Optional[str] = None
    is_active: bool


class AccountListResponse(BaseModel):
    """Schema de resposta para lista de contas."""
    
    accounts: List[AccountResponse]
    total: int
    total_balance: Decimal


# ===========================================
# Credit Card Schemas
# ===========================================

class CreditCardBase(BaseModel):
    """Schema base de cartão de crédito."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Nome do cartão")
    institution: str = Field(..., min_length=1, max_length=255, description="Banco emissor")
    limit: Decimal = Field(..., ge=0, description="Limite do cartão")
    closing_day: int = Field(..., ge=1, le=31, description="Dia do fechamento")
    due_day: int = Field(..., ge=1, le=31, description="Dia do vencimento")
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$", description="Cor em hex")


class CreditCardCreate(CreditCardBase):
    """Schema para criação de cartão."""
    pass


class CreditCardUpdate(BaseModel):
    """Schema para atualização de cartão."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    institution: Optional[str] = Field(None, min_length=1, max_length=255)
    limit: Optional[Decimal] = Field(None, ge=0)
    closing_day: Optional[int] = Field(None, ge=1, le=31)
    due_day: Optional[int] = Field(None, ge=1, le=31)
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    is_active: Optional[bool] = None


class CreditCardResponse(BaseModel):
    """Schema de resposta de cartão."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    name: str
    institution: str
    limit: Decimal
    closing_day: int
    due_day: int
    color: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # Campos calculados (preenchidos pelo service)
    current_invoice: Optional[Decimal] = None
    available_limit: Optional[Decimal] = None


class CreditCardSummary(BaseModel):
    """Schema resumido de cartão."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    institution: str
    limit: Decimal
    closing_day: int
    due_day: int
    color: Optional[str] = None
    is_active: bool


class CreditCardListResponse(BaseModel):
    """Schema de resposta para lista de cartões."""
    
    cards: List[CreditCardResponse]
    total: int
    total_limit: Decimal
