"""
Repository de Contas e Cartões - Camada de acesso a dados.
"""

from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.accounts.models import Account, CreditCard, AccountType


class AccountRepository:
    """Repository para operações de Contas."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, account_id: UUID, user_id: UUID) -> Optional[Account]:
        """Busca conta por ID, garantindo que pertence ao usuário."""
        return (
            self.db.query(Account)
            .filter(Account.id == account_id, Account.user_id == user_id)
            .first()
        )
    
    def get_all_by_user(
        self,
        user_id: UUID,
        include_inactive: bool = False
    ) -> List[Account]:
        """Lista todas as contas do usuário."""
        query = self.db.query(Account).filter(Account.user_id == user_id)
        
        if not include_inactive:
            query = query.filter(Account.is_active == True)
        
        return query.order_by(Account.name).all()
    
    def get_total_balance(self, user_id: UUID) -> Decimal:
        """Calcula saldo total de todas as contas do usuário."""
        result = (
            self.db.query(func.sum(Account.current_balance))
            .filter(Account.user_id == user_id, Account.is_active == True)
            .scalar()
        )
        return result or Decimal("0.00")
    
    def create(self, account: Account) -> Account:
        """Cria nova conta."""
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account
    
    def update(self, account: Account) -> Account:
        """Atualiza conta existente."""
        self.db.commit()
        self.db.refresh(account)
        return account
    
    def delete(self, account: Account) -> None:
        """Remove conta do banco."""
        self.db.delete(account)
        self.db.commit()
    
    def update_balance(self, account_id: UUID, new_balance: Decimal) -> None:
        """Atualiza saldo da conta."""
        self.db.query(Account).filter(Account.id == account_id).update(
            {"current_balance": new_balance}
        )
        self.db.commit()


class CreditCardRepository:
    """Repository para operações de Cartões de Crédito."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, card_id: UUID, user_id: UUID) -> Optional[CreditCard]:
        """Busca cartão por ID, garantindo que pertence ao usuário."""
        return (
            self.db.query(CreditCard)
            .filter(CreditCard.id == card_id, CreditCard.user_id == user_id)
            .first()
        )
    
    def get_all_by_user(
        self,
        user_id: UUID,
        include_inactive: bool = False
    ) -> List[CreditCard]:
        """Lista todos os cartões do usuário."""
        query = self.db.query(CreditCard).filter(CreditCard.user_id == user_id)
        
        if not include_inactive:
            query = query.filter(CreditCard.is_active == True)
        
        return query.order_by(CreditCard.name).all()
    
    def get_total_limit(self, user_id: UUID) -> Decimal:
        """Calcula limite total de todos os cartões do usuário."""
        result = (
            self.db.query(func.sum(CreditCard.limit))
            .filter(CreditCard.user_id == user_id, CreditCard.is_active == True)
            .scalar()
        )
        return result or Decimal("0.00")
    
    def create(self, card: CreditCard) -> CreditCard:
        """Cria novo cartão."""
        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return card
    
    def update(self, card: CreditCard) -> CreditCard:
        """Atualiza cartão existente."""
        self.db.commit()
        self.db.refresh(card)
        return card
    
    def delete(self, card: CreditCard) -> None:
        """Remove cartão do banco."""
        self.db.delete(card)
        self.db.commit()
