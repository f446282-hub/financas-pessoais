"""
Model de Usuário - Entidade principal de autenticação.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """
    Entidade de usuário do sistema.
    
    Attributes:
        id: Identificador único (UUID)
        email: Email do usuário (único)
        password_hash: Hash bcrypt da senha
        name: Nome completo do usuário
        avatar_url: URL da foto de perfil (opcional)
        is_active: Se o usuário está ativo
        created_at: Data de criação
        updated_at: Data da última atualização
    """
    
    __tablename__ = "users"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    password_hash = Column(
        String(255),
        nullable=False,
    )
    name = Column(
        String(255),
        nullable=False,
    )
    avatar_url = Column(
        String(500),
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
    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")
    credit_cards = relationship("CreditCard", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    investment_portfolios = relationship("InvestmentPortfolio", back_populates="user", cascade="all, delete-orphan")
    bank_integrations = relationship("BankIntegration", back_populates="user", cascade="all, delete-orphan")
    whatsapp_settings = relationship("WhatsAppSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"
