"""
Service de Usuário - Regras de negócio.
"""

from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.users.models import User
from app.users.repository import UserRepository
from app.users.schemas import UserCreate, UserUpdate, UserPasswordUpdate
from app.core.security import get_password_hash, verify_password, create_access_token


class UserService:
    """
    Service com regras de negócio relacionadas a Usuários.
    
    Orquestra operações entre repository e aplica validações de negócio.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)
    
    def register(self, data: UserCreate) -> User:
        """
        Registra novo usuário no sistema.
        
        Args:
            data: Dados de criação do usuário
            
        Returns:
            Usuário criado
            
        Raises:
            HTTPException: Se email já existe
        """
        # Verifica se email já está em uso
        if self.repository.email_exists(data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este email já está cadastrado"
            )
        
        # Cria o usuário com senha hasheada
        user = User(
            email=data.email.lower(),
            password_hash=get_password_hash(data.password),
            name=data.name,
        )
        
        return self.repository.create(user)
    
    def authenticate(self, email: str, password: str) -> Optional[User]:
        """
        Autentica usuário por email e senha.
        
        Args:
            email: Email do usuário
            password: Senha em texto plano
            
        Returns:
            Usuário se autenticação bem-sucedida, None caso contrário
        """
        user = self.repository.get_by_email(email)
        
        if not user:
            return None
        
        if not verify_password(password, user.password_hash):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    def login(self, email: str, password: str) -> tuple[User, str]:
        """
        Realiza login e retorna usuário com token.
        
        Args:
            email: Email do usuário
            password: Senha
            
        Returns:
            Tupla com (usuário, token JWT)
            
        Raises:
            HTTPException: Se credenciais inválidas
        """
        user = self.authenticate(email, password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Gera token JWT
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )
        
        return user, access_token
    
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Busca usuário por ID."""
        return self.repository.get_by_id(user_id)
    
    def update(self, user: User, data: UserUpdate) -> User:
        """
        Atualiza dados do usuário.
        
        Args:
            user: Usuário a ser atualizado
            data: Novos dados
            
        Returns:
            Usuário atualizado
        """
        if data.name is not None:
            user.name = data.name
        
        if data.avatar_url is not None:
            user.avatar_url = data.avatar_url
        
        return self.repository.update(user)
    
    def update_password(self, user: User, data: UserPasswordUpdate) -> User:
        """
        Atualiza senha do usuário.
        
        Args:
            user: Usuário
            data: Senha atual e nova
            
        Returns:
            Usuário atualizado
            
        Raises:
            HTTPException: Se senha atual incorreta
        """
        if not verify_password(data.current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Senha atual incorreta"
            )
        
        user.password_hash = get_password_hash(data.new_password)
        return self.repository.update(user)
