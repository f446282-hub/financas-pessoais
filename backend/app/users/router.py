"""
Router de Usuários e Autenticação.
Define endpoints de registro, login e perfil.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import CurrentUser, DatabaseSession
from app.users.service import UserService
from app.users.schemas import (
    UserCreate,
    UserUpdate,
    UserPasswordUpdate,
    UserResponse,
    LoginRequest,
    TokenResponse,
    RegisterResponse,
)


# Router de autenticação
auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])

# Router de usuários
users_router = APIRouter(prefix="/users", tags=["Usuários"])


# ===========================================
# Endpoints de Autenticação
# ===========================================

@auth_router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar novo usuário",
    description="Cria uma nova conta de usuário no sistema.",
)
async def register(
    data: UserCreate,
    db: DatabaseSession,
):
    """
    Registra um novo usuário.
    
    - **email**: Email válido e único
    - **password**: Mínimo 6 caracteres
    - **name**: Nome completo do usuário
    """
    service = UserService(db)
    user = service.register(data)
    
    return RegisterResponse(user=UserResponse.model_validate(user))


@auth_router.post(
    "/login",
    response_model=TokenResponse,
    summary="Fazer login",
    description="Autentica o usuário e retorna um token JWT.",
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DatabaseSession,
):
    """
    Realiza login e retorna token de acesso.
    
    Use o token retornado no header `Authorization: Bearer <token>`
    para acessar endpoints protegidos.
    """
    service = UserService(db)
    user, token = service.login(form_data.username, form_data.password)
    
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@auth_router.post(
    "/login/json",
    response_model=TokenResponse,
    summary="Fazer login (JSON)",
    description="Autentica o usuário via JSON e retorna um token JWT.",
)
async def login_json(
    data: LoginRequest,
    db: DatabaseSession,
):
    """
    Realiza login via JSON (alternativa ao form-data).
    
    Útil para integração com frontends que preferem JSON.
    """
    service = UserService(db)
    user, token = service.login(data.email, data.password)
    
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@auth_router.get(
    "/me",
    response_model=UserResponse,
    summary="Dados do usuário logado",
    description="Retorna os dados do usuário autenticado.",
)
async def get_current_user_data(
    current_user: CurrentUser,
):
    """
    Retorna os dados do usuário atual.
    
    Requer autenticação via token JWT.
    """
    return UserResponse.model_validate(current_user)


# ===========================================
# Endpoints de Perfil
# ===========================================

@users_router.put(
    "/me",
    response_model=UserResponse,
    summary="Atualizar perfil",
    description="Atualiza os dados do perfil do usuário logado.",
)
async def update_profile(
    data: UserUpdate,
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """
    Atualiza nome e/ou avatar do usuário.
    """
    service = UserService(db)
    user = service.update(current_user, data)
    
    return UserResponse.model_validate(user)


@users_router.put(
    "/me/password",
    response_model=UserResponse,
    summary="Alterar senha",
    description="Altera a senha do usuário logado.",
)
async def update_password(
    data: UserPasswordUpdate,
    current_user: CurrentUser,
    db: DatabaseSession,
):
    """
    Altera a senha do usuário.
    
    Requer a senha atual para confirmação.
    """
    service = UserService(db)
    user = service.update_password(current_user, data)
    
    return UserResponse.model_validate(user)
