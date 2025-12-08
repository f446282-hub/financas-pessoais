"""
Schemas Pydantic para validação e serialização de Usuários.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# ===========================================
# Request Schemas (entrada)
# ===========================================

class UserCreate(BaseModel):
    """Schema para criação de usuário (registro)."""
    
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Senha (mínimo 6 caracteres)"
    )
    name: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Nome completo"
    )


class UserUpdate(BaseModel):
    """Schema para atualização de usuário."""
    
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    avatar_url: Optional[str] = Field(None, max_length=500)


class UserPasswordUpdate(BaseModel):
    """Schema para alteração de senha."""
    
    current_password: str = Field(..., description="Senha atual")
    new_password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Nova senha"
    )


# ===========================================
# Response Schemas (saída)
# ===========================================

class UserResponse(BaseModel):
    """Schema de resposta com dados do usuário."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    email: EmailStr
    name: str
    avatar_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserSimple(BaseModel):
    """Schema simplificado do usuário (para listagens)."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    email: EmailStr
    name: str
    avatar_url: Optional[str] = None


# ===========================================
# Auth Schemas
# ===========================================

class LoginRequest(BaseModel):
    """Schema para requisição de login."""
    
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., description="Senha")


class TokenResponse(BaseModel):
    """Schema de resposta com token JWT."""
    
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class RegisterResponse(BaseModel):
    """Schema de resposta para registro."""
    
    message: str = "Usuário criado com sucesso"
    user: UserResponse
