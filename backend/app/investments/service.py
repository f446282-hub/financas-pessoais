"""
Investments module - Schemas, Repository, Service e Router.
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import APIRouter, HTTPException, status, Query

from app.core.dependencies import CurrentUser, DatabaseSession
from app.investments.models import InvestmentPortfolio, InvestmentEntry, InvestmentEntryType


# ===========================================
# Schemas
# ===========================================

class PortfolioCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    type: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None


class PortfolioUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class PortfolioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    name: str
    type: Optional[str] = None
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    total_invested: Optional[Decimal] = None
    current_balance: Optional[Decimal] = None


class EntryCreate(BaseModel):
    type: InvestmentEntryType
    amount: Decimal = Field(..., gt=0)
    date: date
    description: Optional[str] = Field(None, max_length=255)


class EntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    portfolio_id: UUID
    type: InvestmentEntryType
    amount: Decimal
    date: date
    description: Optional[str] = None
    created_at: datetime


# ===========================================
# Repository
# ===========================================

class InvestmentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_portfolio_by_id(self, portfolio_id: UUID, user_id: UUID) -> Optional[InvestmentPortfolio]:
        return self.db.query(InvestmentPortfolio).filter(
            InvestmentPortfolio.id == portfolio_id,
            InvestmentPortfolio.user_id == user_id
        ).first()
    
    def get_all_portfolios(self, user_id: UUID, include_inactive: bool = False) -> List[InvestmentPortfolio]:
        query = self.db.query(InvestmentPortfolio).filter(InvestmentPortfolio.user_id == user_id)
        if not include_inactive:
            query = query.filter(InvestmentPortfolio.is_active == True)
        return query.order_by(InvestmentPortfolio.name).all()
    
    def create_portfolio(self, portfolio: InvestmentPortfolio) -> InvestmentPortfolio:
        self.db.add(portfolio)
        self.db.commit()
        self.db.refresh(portfolio)
        return portfolio
    
    def update_portfolio(self, portfolio: InvestmentPortfolio) -> InvestmentPortfolio:
        self.db.commit()
        self.db.refresh(portfolio)
        return portfolio
    
    def delete_portfolio(self, portfolio: InvestmentPortfolio) -> None:
        self.db.delete(portfolio)
        self.db.commit()
    
    def get_entries(self, portfolio_id: UUID) -> List[InvestmentEntry]:
        return self.db.query(InvestmentEntry).filter(
            InvestmentEntry.portfolio_id == portfolio_id
        ).order_by(InvestmentEntry.date.desc()).all()
    
    def create_entry(self, entry: InvestmentEntry) -> InvestmentEntry:
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry
    
    def calculate_portfolio_balance(self, portfolio_id: UUID) -> dict:
        deposits = self.db.query(func.sum(InvestmentEntry.amount)).filter(
            InvestmentEntry.portfolio_id == portfolio_id,
            InvestmentEntry.type == InvestmentEntryType.DEPOSIT
        ).scalar() or Decimal("0.00")
        
        withdrawals = self.db.query(func.sum(InvestmentEntry.amount)).filter(
            InvestmentEntry.portfolio_id == portfolio_id,
            InvestmentEntry.type == InvestmentEntryType.WITHDRAWAL
        ).scalar() or Decimal("0.00")
        
        return {
            "total_invested": deposits,
            "total_withdrawn": withdrawals,
            "current_balance": deposits - withdrawals,
        }


# ===========================================
# Service
# ===========================================

class InvestmentService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = InvestmentRepository(db)
    
    def create_portfolio(self, user_id: UUID, data: PortfolioCreate) -> InvestmentPortfolio:
        portfolio = InvestmentPortfolio(
            user_id=user_id,
            name=data.name,
            type=data.type,
            description=data.description,
        )
        return self.repository.create_portfolio(portfolio)
    
    def get_portfolio(self, portfolio_id: UUID, user_id: UUID) -> InvestmentPortfolio:
        portfolio = self.repository.get_portfolio_by_id(portfolio_id, user_id)
        if not portfolio:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não encontrada")
        return portfolio
    
    def get_all_portfolios(self, user_id: UUID, include_inactive: bool = False) -> List[dict]:
        portfolios = self.repository.get_all_portfolios(user_id, include_inactive)
        result = []
        for p in portfolios:
            balance = self.repository.calculate_portfolio_balance(p.id)
            data = PortfolioResponse.model_validate(p).model_dump()
            data["total_invested"] = balance["total_invested"]
            data["current_balance"] = balance["current_balance"]
            result.append(data)
        return result
    
    def update_portfolio(self, portfolio_id: UUID, user_id: UUID, data: PortfolioUpdate) -> InvestmentPortfolio:
        portfolio = self.get_portfolio(portfolio_id, user_id)
        if data.name is not None:
            portfolio.name = data.name
        if data.type is not None:
            portfolio.type = data.type
        if data.description is not None:
            portfolio.description = data.description
        if data.is_active is not None:
            portfolio.is_active = data.is_active
        return self.repository.update_portfolio(portfolio)
    
    def delete_portfolio(self, portfolio_id: UUID, user_id: UUID) -> None:
        portfolio = self.get_portfolio(portfolio_id, user_id)
        self.repository.delete_portfolio(portfolio)
    
    def add_entry(self, portfolio_id: UUID, user_id: UUID, data: EntryCreate) -> InvestmentEntry:
        self.get_portfolio(portfolio_id, user_id)  # Verifica se existe
        entry = InvestmentEntry(
            portfolio_id=portfolio_id,
            type=data.type,
            amount=data.amount,
            date=data.date,
            description=data.description,
        )
        return self.repository.create_entry(entry)
    
    def get_entries(self, portfolio_id: UUID, user_id: UUID) -> List[InvestmentEntry]:
        self.get_portfolio(portfolio_id, user_id)
        return self.repository.get_entries(portfolio_id)


# ===========================================
# Router
# ===========================================

investments_router = APIRouter(prefix="/investments", tags=["Investimentos"])


@investments_router.get("/portfolios", response_model=List[PortfolioResponse])
async def list_portfolios(current_user: CurrentUser, db: DatabaseSession, include_inactive: bool = False):
    """Lista todas as carteiras de investimento."""
    service = InvestmentService(db)
    return service.get_all_portfolios(current_user.id, include_inactive)


@investments_router.post("/portfolios", response_model=PortfolioResponse, status_code=status.HTTP_201_CREATED)
async def create_portfolio(data: PortfolioCreate, current_user: CurrentUser, db: DatabaseSession):
    """Cria nova carteira de investimento."""
    service = InvestmentService(db)
    portfolio = service.create_portfolio(current_user.id, data)
    balance = service.repository.calculate_portfolio_balance(portfolio.id)
    response = PortfolioResponse.model_validate(portfolio)
    response.total_invested = balance["total_invested"]
    response.current_balance = balance["current_balance"]
    return response


@investments_router.get("/portfolios/{portfolio_id}", response_model=PortfolioResponse)
async def get_portfolio(portfolio_id: UUID, current_user: CurrentUser, db: DatabaseSession):
    """Retorna detalhes de uma carteira."""
    service = InvestmentService(db)
    portfolio = service.get_portfolio(portfolio_id, current_user.id)
    balance = service.repository.calculate_portfolio_balance(portfolio.id)
    response = PortfolioResponse.model_validate(portfolio)
    response.total_invested = balance["total_invested"]
    response.current_balance = balance["current_balance"]
    return response


@investments_router.put("/portfolios/{portfolio_id}", response_model=PortfolioResponse)
async def update_portfolio(portfolio_id: UUID, data: PortfolioUpdate, current_user: CurrentUser, db: DatabaseSession):
    """Atualiza uma carteira."""
    service = InvestmentService(db)
    portfolio = service.update_portfolio(portfolio_id, current_user.id, data)
    return PortfolioResponse.model_validate(portfolio)


@investments_router.delete("/portfolios/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_portfolio(portfolio_id: UUID, current_user: CurrentUser, db: DatabaseSession):
    """Remove uma carteira."""
    service = InvestmentService(db)
    service.delete_portfolio(portfolio_id, current_user.id)


@investments_router.get("/portfolios/{portfolio_id}/entries", response_model=List[EntryResponse])
async def list_entries(portfolio_id: UUID, current_user: CurrentUser, db: DatabaseSession):
    """Lista movimentações de uma carteira."""
    service = InvestmentService(db)
    entries = service.get_entries(portfolio_id, current_user.id)
    return [EntryResponse.model_validate(e) for e in entries]


@investments_router.post("/portfolios/{portfolio_id}/entries", response_model=EntryResponse, status_code=status.HTTP_201_CREATED)
async def create_entry(portfolio_id: UUID, data: EntryCreate, current_user: CurrentUser, db: DatabaseSession):
    """Registra aporte ou resgate em uma carteira."""
    service = InvestmentService(db)
    entry = service.add_entry(portfolio_id, current_user.id, data)
    return EntryResponse.model_validate(entry)
