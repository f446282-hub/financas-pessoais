"""
Integrations module - Integrações com bancos e WhatsApp.
"""

import uuid
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum as PyEnum
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Column, String, Boolean, DateTime, Numeric, Enum, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Session, relationship
from fastapi import APIRouter, HTTPException, status

from app.core.database import Base
from app.core.dependencies import CurrentUser, DatabaseSession


# ===========================================
# Models
# ===========================================

class IntegrationStatus(str, PyEnum):
    DISCONNECTED = "disconnected"
    CONNECTED = "connected"
    ERROR = "error"


class BankIntegration(Base):
    """Integração com banco."""
    
    __tablename__ = "bank_integrations"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    provider = Column(String(100), nullable=False)
    status = Column(Enum(IntegrationStatus), nullable=False, default=IntegrationStatus.DISCONNECTED)
    connected_at = Column(DateTime(timezone=True), nullable=True)
    last_sync_at = Column(DateTime(timezone=True), nullable=True)
    config = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    user = relationship("User", back_populates="bank_integrations")


class WhatsAppSettings(Base):
    """Configurações de integração WhatsApp."""
    
    __tablename__ = "whatsapp_settings"
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    phone_number = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=False, nullable=False)
    alert_on_high_expense = Column(Boolean, default=False, nullable=False)
    high_expense_threshold = Column(Numeric(15, 2), nullable=True)
    daily_summary = Column(Boolean, default=False, nullable=False)
    weekly_summary = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    user = relationship("User", back_populates="whatsapp_settings")


# ===========================================
# Schemas
# ===========================================

class BankIntegrationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    provider: str
    status: IntegrationStatus
    connected_at: Optional[datetime] = None
    last_sync_at: Optional[datetime] = None


class BankProvider(BaseModel):
    code: str
    name: str
    logo_url: Optional[str] = None
    available: bool = True


class WhatsAppSettingsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: Optional[UUID] = None
    phone_number: Optional[str] = None
    is_active: bool = False
    alert_on_high_expense: bool = False
    high_expense_threshold: Optional[Decimal] = None
    daily_summary: bool = False
    weekly_summary: bool = False


class WhatsAppSettingsUpdate(BaseModel):
    phone_number: Optional[str] = Field(None, pattern=r"^\+?[0-9]{10,15}$")
    is_active: Optional[bool] = None
    alert_on_high_expense: Optional[bool] = None
    high_expense_threshold: Optional[Decimal] = Field(None, ge=0)
    daily_summary: Optional[bool] = None
    weekly_summary: Optional[bool] = None


# ===========================================
# Service
# ===========================================

class IntegrationService:
    """Gerencia integrações com serviços externos."""
    
    BANK_PROVIDERS = [
        {"code": "nubank", "name": "Nubank", "logo_url": "/images/banks/nubank.svg", "available": True},
        {"code": "itau", "name": "Itaú", "logo_url": "/images/banks/itau.svg", "available": True},
        {"code": "bradesco", "name": "Bradesco", "logo_url": "/images/banks/bradesco.svg", "available": True},
        {"code": "santander", "name": "Santander", "logo_url": "/images/banks/santander.svg", "available": True},
        {"code": "bb", "name": "Banco do Brasil", "logo_url": "/images/banks/bb.svg", "available": True},
        {"code": "caixa", "name": "Caixa", "logo_url": "/images/banks/caixa.svg", "available": True},
        {"code": "inter", "name": "Banco Inter", "logo_url": "/images/banks/inter.svg", "available": True},
        {"code": "c6", "name": "C6 Bank", "logo_url": "/images/banks/c6.svg", "available": True},
        {"code": "open_finance", "name": "Open Finance", "logo_url": "/images/banks/open-finance.svg", "available": True},
    ]
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_bank_providers(self) -> List[BankProvider]:
        """Lista provedores de banco disponíveis."""
        return [BankProvider(**p) for p in self.BANK_PROVIDERS]
    
    def get_user_bank_integrations(self, user_id: UUID) -> List[BankIntegration]:
        """Lista integrações bancárias do usuário."""
        return self.db.query(BankIntegration).filter(BankIntegration.user_id == user_id).all()
    
    def connect_bank(self, user_id: UUID, provider: str) -> BankIntegration:
        """Inicia conexão com um banco."""
        # Verifica se provedor existe
        valid_providers = [p["code"] for p in self.BANK_PROVIDERS]
        if provider not in valid_providers:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provedor não suportado")
        
        # Verifica se já existe integração
        existing = self.db.query(BankIntegration).filter(
            BankIntegration.user_id == user_id,
            BankIntegration.provider == provider
        ).first()
        
        if existing:
            existing.status = IntegrationStatus.CONNECTED
            existing.connected_at = datetime.now(timezone.utc)
            self.db.commit()
            return existing
        
        # Cria nova integração
        integration = BankIntegration(
            user_id=user_id,
            provider=provider,
            status=IntegrationStatus.CONNECTED,
            connected_at=datetime.now(timezone.utc),
        )
        self.db.add(integration)
        self.db.commit()
        self.db.refresh(integration)
        return integration
    
    def disconnect_bank(self, user_id: UUID, provider: str) -> None:
        """Desconecta integração com banco."""
        integration = self.db.query(BankIntegration).filter(
            BankIntegration.user_id == user_id,
            BankIntegration.provider == provider
        ).first()
        
        if integration:
            integration.status = IntegrationStatus.DISCONNECTED
            integration.connected_at = None
            self.db.commit()
    
    def sync_bank(self, user_id: UUID, provider: str) -> BankIntegration:
        """Sincroniza dados com o banco."""
        integration = self.db.query(BankIntegration).filter(
            BankIntegration.user_id == user_id,
            BankIntegration.provider == provider
        ).first()
        
        if not integration or integration.status != IntegrationStatus.CONNECTED:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Banco não conectado")
        
        # Simula sincronização
        integration.last_sync_at = datetime.now(timezone.utc)
        self.db.commit()
        return integration
    
    def get_whatsapp_settings(self, user_id: UUID) -> Optional[WhatsAppSettings]:
        """Retorna configurações de WhatsApp do usuário."""
        return self.db.query(WhatsAppSettings).filter(WhatsAppSettings.user_id == user_id).first()
    
    def update_whatsapp_settings(self, user_id: UUID, data: WhatsAppSettingsUpdate) -> WhatsAppSettings:
        """Atualiza configurações de WhatsApp."""
        settings = self.get_whatsapp_settings(user_id)
        
        if not settings:
            settings = WhatsAppSettings(user_id=user_id)
            self.db.add(settings)
        
        if data.phone_number is not None:
            settings.phone_number = data.phone_number
        if data.is_active is not None:
            settings.is_active = data.is_active
        if data.alert_on_high_expense is not None:
            settings.alert_on_high_expense = data.alert_on_high_expense
        if data.high_expense_threshold is not None:
            settings.high_expense_threshold = data.high_expense_threshold
        if data.daily_summary is not None:
            settings.daily_summary = data.daily_summary
        if data.weekly_summary is not None:
            settings.weekly_summary = data.weekly_summary
        
        self.db.commit()
        self.db.refresh(settings)
        return settings


# ===========================================
# Router
# ===========================================

integrations_router = APIRouter(prefix="/integrations", tags=["Integrações"])


@integrations_router.get("/banks/providers", response_model=List[BankProvider])
async def list_bank_providers(current_user: CurrentUser, db: DatabaseSession):
    """Lista bancos disponíveis para integração."""
    service = IntegrationService(db)
    return service.get_bank_providers()


@integrations_router.get("/banks", response_model=List[BankIntegrationResponse])
async def list_bank_integrations(current_user: CurrentUser, db: DatabaseSession):
    """Lista integrações bancárias do usuário."""
    service = IntegrationService(db)
    integrations = service.get_user_bank_integrations(current_user.id)
    return [BankIntegrationResponse.model_validate(i) for i in integrations]


@integrations_router.post("/banks/{provider}/connect", response_model=BankIntegrationResponse)
async def connect_bank(provider: str, current_user: CurrentUser, db: DatabaseSession):
    """Conecta com um banco."""
    service = IntegrationService(db)
    integration = service.connect_bank(current_user.id, provider)
    return BankIntegrationResponse.model_validate(integration)


@integrations_router.post("/banks/{provider}/disconnect", status_code=status.HTTP_204_NO_CONTENT)
async def disconnect_bank(provider: str, current_user: CurrentUser, db: DatabaseSession):
    """Desconecta de um banco."""
    service = IntegrationService(db)
    service.disconnect_bank(current_user.id, provider)


@integrations_router.post("/banks/{provider}/sync", response_model=BankIntegrationResponse)
async def sync_bank(provider: str, current_user: CurrentUser, db: DatabaseSession):
    """Sincroniza dados com o banco."""
    service = IntegrationService(db)
    integration = service.sync_bank(current_user.id, provider)
    return BankIntegrationResponse.model_validate(integration)


@integrations_router.get("/whatsapp", response_model=WhatsAppSettingsResponse)
async def get_whatsapp_settings(current_user: CurrentUser, db: DatabaseSession):
    """Retorna configurações de WhatsApp."""
    service = IntegrationService(db)
    settings = service.get_whatsapp_settings(current_user.id)
    if not settings:
        return WhatsAppSettingsResponse()
    return WhatsAppSettingsResponse.model_validate(settings)


@integrations_router.put("/whatsapp", response_model=WhatsAppSettingsResponse)
async def update_whatsapp_settings(data: WhatsAppSettingsUpdate, current_user: CurrentUser, db: DatabaseSession):
    """Atualiza configurações de WhatsApp."""
    service = IntegrationService(db)
    settings = service.update_whatsapp_settings(current_user.id, data)
    return WhatsAppSettingsResponse.model_validate(settings)
