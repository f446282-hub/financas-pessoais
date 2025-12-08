"""
Models de Investimentos - Carteiras e Movimentações.
"""

import uuid
from datetime import datetime, date, timezone
from decimal import Decimal
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Boolean, DateTime, Date, Numeric, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class InvestmentEntryType(str, PyEnum):
    """Tipos de movimentação de investimento."""
    DEPOSIT = "deposit"        # Aporte
    WITHDRAWAL = "withdrawal"  # Resgate


class InvestmentPortfolio(Base):
    """Carteira de Investimentos."""
    
    __tablename__ = "investment_portfolios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=True)  # Renda Fixa, Ações, Misto, etc.
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relacionamentos
    user = relationship("User", back_populates="investment_portfolios")
    entries = relationship("InvestmentEntry", back_populates="portfolio", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<InvestmentPortfolio(id={self.id}, name={self.name})>"


class InvestmentEntry(Base):
    """Movimentação de Investimento (Aporte/Resgate)."""
    
    __tablename__ = "investment_entries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey("investment_portfolios.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(Enum(InvestmentEntryType), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    date = Column(Date, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relacionamentos
    portfolio = relationship("InvestmentPortfolio", back_populates="entries")
    
    def __repr__(self) -> str:
        return f"<InvestmentEntry(id={self.id}, type={self.type}, amount={self.amount})>"
