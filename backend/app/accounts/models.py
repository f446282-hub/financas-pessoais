"""
Models de Contas Bancárias e Cartões de Crédito.
"""

import uuid
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Boolean, DateTime, Numeric, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class AccountType(str, PyEnum):
    """Tipos de conta disponíveis."""
    CHECKING = "checking"      # Conta corrente
    SAVINGS = "savings"        # Poupança
    WALLET = "wallet"          # Carteira física/digital
    INVESTMENT = "investment"  # Conta investimento
    OTHER = "other"            # Outros


class Account(Base):
    """
    Entidade de Conta Bancária/Financeira.
    
    Representa contas correntes, poupanças, carteiras, etc.
    """
    
    __tablename__ = "accounts"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = Column(
        String(255),
        nullable=False,
    )
    type = Column(
        Enum(AccountType),
        nullable=False,
        default=AccountType.CHECKING,
    )
    institution = Column(
        String(255),
        nullable=True,
    )
    initial_balance = Column(
        Numeric(15, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
    current_balance = Column(
        Numeric(15, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
    color = Column(
        String(7),  # Hex color: #RRGGBB
        nullable=True,
    )
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    
    # Relacionamentos
    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Account(id={self.id}, name={self.name}, type={self.type})>"


class CreditCard(Base):
    """
    Entidade de Cartão de Crédito.
    
    Representa cartões de crédito com limite, fechamento e vencimento.
    """
    
    __tablename__ = "credit_cards"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = Column(
        String(255),
        nullable=False,
    )
    institution = Column(
        String(255),
        nullable=False,
    )
    limit = Column(
        Numeric(15, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
    closing_day = Column(
        Integer,
        nullable=False,
    )
    due_day = Column(
        Integer,
        nullable=False,
    )
    color = Column(
        String(7),
        nullable=True,
    )
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    
    # Relacionamentos
    user = relationship("User", back_populates="credit_cards")
    transactions = relationship("Transaction", back_populates="credit_card", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<CreditCard(id={self.id}, name={self.name}, institution={self.institution})>"
