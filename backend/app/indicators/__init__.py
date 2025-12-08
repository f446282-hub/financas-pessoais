"""
Indicators module - Indicadores financeiros.
"""

import uuid
from datetime import datetime, date, timezone
from decimal import Decimal
from enum import Enum as PyEnum
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Session
from fastapi import APIRouter, Query

from app.core.database import Base
from app.core.dependencies import CurrentUser, DatabaseSession


# ===========================================
# Models
# ===========================================

class IndicatorType(str, PyEnum):
    PERCENTAGE = "percentage"
    CURRENCY = "currency"
    NUMBER = "number"


class Indicator(Base):
    """Indicador financeiro."""
    
    __tablename__ = "indicators"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(PGUUID(as_uuid=True), nullable=True, index=True)  # None = global
    name = Column(String(255), nullable=False)
    code = Column(String(100), nullable=False, unique=True)
    description = Column(String(500), nullable=True)
    type = Column(Enum(IndicatorType), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


# ===========================================
# Schemas
# ===========================================

class IndicatorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    code: str
    description: Optional[str] = None
    type: IndicatorType


class IndicatorValue(BaseModel):
    code: str
    name: str
    value: Decimal
    type: IndicatorType
    formatted_value: str


class IndicatorListResponse(BaseModel):
    indicators: List[IndicatorValue]
    period_start: date
    period_end: date


# ===========================================
# Service
# ===========================================

class IndicatorService:
    """Calcula indicadores financeiros."""
    
    # Indicadores padrão do sistema
    DEFAULT_INDICATORS = [
        {"code": "income_committed_pct", "name": "% Renda Comprometida", "type": IndicatorType.PERCENTAGE, 
         "description": "Percentual da renda comprometido com despesas"},
        {"code": "income_invested_pct", "name": "% Renda Investida", "type": IndicatorType.PERCENTAGE,
         "description": "Percentual da renda direcionado para investimentos"},
        {"code": "monthly_savings", "name": "Poupança do Mês", "type": IndicatorType.CURRENCY,
         "description": "Valor economizado no mês (receitas - despesas)"},
        {"code": "expense_count", "name": "Qtd. Despesas", "type": IndicatorType.NUMBER,
         "description": "Quantidade de despesas no período"},
    ]
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_indicators(
        self, 
        user_id: UUID, 
        start_date: date, 
        end_date: date
    ) -> List[IndicatorValue]:
        """Calcula todos os indicadores para o período."""
        from app.transactions.repository import TransactionRepository
        from app.transactions.models import TransactionType
        
        tx_repo = TransactionRepository(self.db)
        totals = tx_repo.get_totals_by_type(user_id, start_date, end_date)
        count = tx_repo.count_by_user(user_id, start_date, end_date, TransactionType.EXPENSE)
        
        income = totals["income"]
        expense = totals["expense"]
        
        results = []
        
        # % Renda Comprometida
        committed_pct = (expense / income * 100) if income > 0 else Decimal("0")
        results.append(IndicatorValue(
            code="income_committed_pct",
            name="% Renda Comprometida",
            value=committed_pct.quantize(Decimal("0.01")),
            type=IndicatorType.PERCENTAGE,
            formatted_value=f"{committed_pct:.1f}%"
        ))
        
        # % Renda Investida (simplificado - considera sobra como investimento potencial)
        savings = income - expense
        invested_pct = (savings / income * 100) if income > 0 and savings > 0 else Decimal("0")
        results.append(IndicatorValue(
            code="income_invested_pct",
            name="% Renda Disponível",
            value=invested_pct.quantize(Decimal("0.01")),
            type=IndicatorType.PERCENTAGE,
            formatted_value=f"{invested_pct:.1f}%"
        ))
        
        # Poupança do Mês
        results.append(IndicatorValue(
            code="monthly_savings",
            name="Saldo do Período",
            value=savings,
            type=IndicatorType.CURRENCY,
            formatted_value=f"R$ {savings:,.2f}"
        ))
        
        # Quantidade de Despesas
        results.append(IndicatorValue(
            code="expense_count",
            name="Qtd. Despesas",
            value=Decimal(count),
            type=IndicatorType.NUMBER,
            formatted_value=str(count)
        ))
        
        return results


# ===========================================
# Router
# ===========================================

indicators_router = APIRouter(prefix="/indicators", tags=["Indicadores"])


@indicators_router.get("", response_model=List[IndicatorResponse])
async def list_indicators(current_user: CurrentUser, db: DatabaseSession):
    """Lista indicadores disponíveis."""
    return [
        IndicatorResponse(
            id=uuid.uuid4(),  # Placeholder
            **ind
        )
        for ind in IndicatorService.DEFAULT_INDICATORS
    ]


@indicators_router.get("/values", response_model=IndicatorListResponse)
async def get_indicator_values(
    current_user: CurrentUser,
    db: DatabaseSession,
    start_date: date = Query(...),
    end_date: date = Query(...),
):
    """Calcula valores dos indicadores para o período."""
    service = IndicatorService(db)
    indicators = service.calculate_indicators(current_user.id, start_date, end_date)
    
    return IndicatorListResponse(
        indicators=indicators,
        period_start=start_date,
        period_end=end_date,
    )
