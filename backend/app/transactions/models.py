"""
Models de Transações (Lançamentos) e Categorias.
"""

import uuid
from datetime import datetime, date, timezone
from decimal import Decimal
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Boolean, DateTime, Date, Numeric, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class TransactionType(str, PyEnum):
    """Tipos de transação."""
    INCOME = "income"    # Receita
    EXPENSE = "expense"  # Despesa


class TransactionStatus(str, PyEnum):
    """Status da transação."""
    PENDING = "pending"      # Pendente
    PAID = "paid"            # Pago/Efetivado
    CANCELLED = "cancelled"  # Cancelado


class Category(Base):
    """
    Entidade de Categoria de Transação.
    
    Categorias podem ser globais (user_id=None) ou personalizadas pelo usuário.
    """
    
    __tablename__ = "categories"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,  # None = categoria global
        index=True,
    )
    name = Column(
        String(100),
        nullable=False,
    )
    type = Column(
        Enum(TransactionType),
        nullable=False,
    )
    icon = Column(
        String(50),
        nullable=True,
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
    
    # Relacionamentos
    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")
    
    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name={self.name}, type={self.type})>"


class Transaction(Base):
    """
    Entidade de Transação (Lançamento Financeiro).
    
    Representa receitas e despesas vinculadas a contas ou cartões.
    """
    
    __tablename__ = "transactions"
    
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
    account_id = Column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=True,  # Pode ser null se for cartão
        index=True,
    )
    credit_card_id = Column(
        UUID(as_uuid=True),
        ForeignKey("credit_cards.id", ondelete="CASCADE"),
        nullable=True,  # Pode ser null se for conta
        index=True,
    )
    category_id = Column(
        UUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    type = Column(
        Enum(TransactionType),
        nullable=False,
        index=True,
    )
    description = Column(
        String(255),
        nullable=False,
    )
    amount = Column(
        Numeric(15, 2),
        nullable=False,
    )
    date = Column(
        Date,
        nullable=False,
        index=True,
    )
    status = Column(
        Enum(TransactionStatus),
        nullable=False,
        default=TransactionStatus.PAID,
    )
    is_recurring = Column(
        Boolean,
        default=False,
        nullable=False,
    )
    recurring_id = Column(
        UUID(as_uuid=True),
        nullable=True,
        index=True,
    )
    notes = Column(
        Text,
        nullable=True,
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
    user = relationship("User", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")
    credit_card = relationship("CreditCard", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
    
    def __repr__(self) -> str:
        return f"<Transaction(id={self.id}, type={self.type}, amount={self.amount})>"
