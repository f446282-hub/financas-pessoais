"""
Repository de Usuário - Camada de acesso a dados.
"""

from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.users.models import User


class UserRepository:
    """
    Repository para operações de banco de dados relacionadas a Usuários.
    
    Encapsula toda a lógica de acesso a dados, mantendo o service limpo.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: UUID | str) -> Optional[User]:
        """Busca usuário por ID."""
        if isinstance(user_id, str):
            user_id = UUID(user_id)
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email."""
        return self.db.query(User).filter(User.email == email.lower()).first()
    
    def email_exists(self, email: str) -> bool:
        """Verifica se email já está cadastrado."""
        return self.db.query(User).filter(User.email == email.lower()).first() is not None
    
    def create(self, user: User) -> User:
        """Cria novo usuário no banco."""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user: User) -> User:
        """Atualiza usuário existente."""
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user: User) -> None:
        """Remove usuário do banco."""
        self.db.delete(user)
        self.db.commit()
