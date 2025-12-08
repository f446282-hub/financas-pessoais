"""
Service de Contas e Cartões - Regras de negócio.
"""

from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.accounts.models import Account, CreditCard
from app.accounts.repository import AccountRepository, CreditCardRepository
from app.accounts.schemas import (
    AccountCreate,
    AccountUpdate,
    CreditCardCreate,
    CreditCardUpdate,
)


class AccountService:
    """Service com regras de negócio de Contas."""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = AccountRepository(db)
    
    def create(self, user_id: UUID, data: AccountCreate) -> Account:
        """
        Cria nova conta para o usuário.
        
        O saldo atual inicial é igual ao saldo inicial informado.
        """
        account = Account(
            user_id=user_id,
            name=data.name,
            type=data.type,
            institution=data.institution,
            initial_balance=data.initial_balance,
            current_balance=data.initial_balance,  # Saldo atual = inicial
            color=data.color,
        )
        
        return self.repository.create(account)
    
    def get_by_id(self, account_id: UUID, user_id: UUID) -> Account:
        """Busca conta por ID."""
        account = self.repository.get_by_id(account_id, user_id)
        
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conta não encontrada"
            )
        
        return account
    
    def get_all(self, user_id: UUID, include_inactive: bool = False) -> List[Account]:
        """Lista todas as contas do usuário."""
        return self.repository.get_all_by_user(user_id, include_inactive)
    
    def get_total_balance(self, user_id: UUID) -> Decimal:
        """Retorna saldo total de todas as contas."""
        return self.repository.get_total_balance(user_id)
    
    def update(self, account_id: UUID, user_id: UUID, data: AccountUpdate) -> Account:
        """Atualiza conta existente."""
        account = self.get_by_id(account_id, user_id)
        
        if data.name is not None:
            account.name = data.name
        if data.type is not None:
            account.type = data.type
        if data.institution is not None:
            account.institution = data.institution
        if data.color is not None:
            account.color = data.color
        if data.is_active is not None:
            account.is_active = data.is_active
        
        return self.repository.update(account)
    
    def delete(self, account_id: UUID, user_id: UUID) -> None:
        """Remove conta."""
        account = self.get_by_id(account_id, user_id)
        self.repository.delete(account)
    
    def recalculate_balance(self, account_id: UUID) -> Decimal:
        """
        Recalcula o saldo da conta baseado nas transações.
        
        Saldo = Saldo inicial + Receitas - Despesas
        """
        # Import aqui para evitar circular import
        from app.transactions.repository import TransactionRepository
        
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            return Decimal("0.00")
        
        tx_repo = TransactionRepository(self.db)
        balance = tx_repo.calculate_account_balance(account_id)
        
        new_balance = account.initial_balance + balance
        self.repository.update_balance(account_id, new_balance)
        
        return new_balance


class CreditCardService:
    """Service com regras de negócio de Cartões de Crédito."""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = CreditCardRepository(db)
    
    def create(self, user_id: UUID, data: CreditCardCreate) -> CreditCard:
        """Cria novo cartão para o usuário."""
        card = CreditCard(
            user_id=user_id,
            name=data.name,
            institution=data.institution,
            limit=data.limit,
            closing_day=data.closing_day,
            due_day=data.due_day,
            color=data.color,
        )
        
        return self.repository.create(card)
    
    def get_by_id(self, card_id: UUID, user_id: UUID) -> CreditCard:
        """Busca cartão por ID."""
        card = self.repository.get_by_id(card_id, user_id)
        
        if not card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cartão não encontrado"
            )
        
        return card
    
    def get_all(self, user_id: UUID, include_inactive: bool = False) -> List[CreditCard]:
        """Lista todos os cartões do usuário."""
        return self.repository.get_all_by_user(user_id, include_inactive)
    
    def get_total_limit(self, user_id: UUID) -> Decimal:
        """Retorna limite total de todos os cartões."""
        return self.repository.get_total_limit(user_id)
    
    def update(self, card_id: UUID, user_id: UUID, data: CreditCardUpdate) -> CreditCard:
        """Atualiza cartão existente."""
        card = self.get_by_id(card_id, user_id)
        
        if data.name is not None:
            card.name = data.name
        if data.institution is not None:
            card.institution = data.institution
        if data.limit is not None:
            card.limit = data.limit
        if data.closing_day is not None:
            card.closing_day = data.closing_day
        if data.due_day is not None:
            card.due_day = data.due_day
        if data.color is not None:
            card.color = data.color
        if data.is_active is not None:
            card.is_active = data.is_active
        
        return self.repository.update(card)
    
    def delete(self, card_id: UUID, user_id: UUID) -> None:
        """Remove cartão."""
        card = self.get_by_id(card_id, user_id)
        self.repository.delete(card)
    
    def get_current_invoice(self, card_id: UUID, user_id: UUID) -> Decimal:
        """
        Calcula valor da fatura atual do cartão.
        
        Considera transações desde o último fechamento até hoje.
        """
        # Import aqui para evitar circular import
        from app.transactions.repository import TransactionRepository
        
        tx_repo = TransactionRepository(self.db)
        return tx_repo.calculate_card_invoice(card_id)
