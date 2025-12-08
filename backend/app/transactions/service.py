"""
Service de Transações e Categorias - Regras de negócio.
"""

from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.transactions.models import Transaction, Category, TransactionType, TransactionStatus
from app.transactions.repository import TransactionRepository, CategoryRepository
from app.transactions.schemas import (
    TransactionCreate,
    TransactionUpdate,
    TransactionSummary,
    CategoryCreate,
)
from app.accounts.service import AccountService


class CategoryService:
    """Service com regras de negócio de Categorias."""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = CategoryRepository(db)
    
    def get_all(self, user_id: UUID) -> List[Category]:
        """Lista todas as categorias disponíveis para o usuário."""
        return self.repository.get_all_for_user(user_id)
    
    def get_by_type(self, user_id: UUID, tx_type: TransactionType) -> List[Category]:
        """Lista categorias de um tipo específico."""
        return self.repository.get_by_type(user_id, tx_type)
    
    def create(self, user_id: UUID, data: CategoryCreate) -> Category:
        """Cria nova categoria personalizada para o usuário."""
        category = Category(
            user_id=user_id,
            name=data.name,
            type=data.type,
            icon=data.icon,
            color=data.color,
        )
        return self.repository.create(category)
    
    def ensure_default_categories_exist(self) -> None:
        """Garante que categorias padrão existam."""
        existing = self.db.query(Category).filter(Category.user_id == None).first()
        if not existing:
            self.repository.create_default_categories()


class TransactionService:
    """Service com regras de negócio de Transações."""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = TransactionRepository(db)
    
    def create(self, user_id: UUID, data: TransactionCreate) -> Transaction:
        """
        Cria nova transação.
        
        Após criar, recalcula o saldo da conta (se aplicável).
        """
        transaction = Transaction(
            user_id=user_id,
            account_id=data.account_id,
            credit_card_id=data.credit_card_id,
            category_id=data.category_id,
            type=data.type,
            description=data.description,
            amount=data.amount,
            date=data.date,
            status=data.status,
            is_recurring=data.is_recurring,
            notes=data.notes,
        )
        
        transaction = self.repository.create(transaction)
        
        # Recalcular saldo da conta
        if transaction.account_id:
            account_service = AccountService(self.db)
            account_service.recalculate_balance(transaction.account_id)
        
        return transaction
    
    def get_by_id(self, transaction_id: UUID, user_id: UUID) -> Transaction:
        """Busca transação por ID."""
        transaction = self.repository.get_by_id(transaction_id, user_id)
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transação não encontrada"
            )
        
        return transaction
    
    def get_all(
        self,
        user_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        tx_type: Optional[TransactionType] = None,
        status: Optional[TransactionStatus] = None,
        account_id: Optional[UUID] = None,
        credit_card_id: Optional[UUID] = None,
        category_id: Optional[UUID] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Transaction]:
        """Lista transações com filtros."""
        return self.repository.get_all_by_user(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            tx_type=tx_type,
            status=status,
            account_id=account_id,
            credit_card_id=credit_card_id,
            category_id=category_id,
            limit=limit,
            offset=offset,
        )
    
    def update(self, transaction_id: UUID, user_id: UUID, data: TransactionUpdate) -> Transaction:
        """Atualiza transação existente."""
        transaction = self.get_by_id(transaction_id, user_id)
        old_account_id = transaction.account_id
        
        if data.description is not None:
            transaction.description = data.description
        if data.amount is not None:
            transaction.amount = data.amount
        if data.date is not None:
            transaction.date = data.date
        if data.status is not None:
            transaction.status = data.status
        if data.category_id is not None:
            transaction.category_id = data.category_id
        if data.notes is not None:
            transaction.notes = data.notes
        
        transaction = self.repository.update(transaction)
        
        # Recalcular saldo da conta
        if old_account_id:
            account_service = AccountService(self.db)
            account_service.recalculate_balance(old_account_id)
        
        return transaction
    
    def delete(self, transaction_id: UUID, user_id: UUID) -> None:
        """Remove transação."""
        transaction = self.get_by_id(transaction_id, user_id)
        account_id = transaction.account_id
        
        self.repository.delete(transaction)
        
        # Recalcular saldo da conta
        if account_id:
            account_service = AccountService(self.db)
            account_service.recalculate_balance(account_id)
    
    def get_summary(
        self,
        user_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> TransactionSummary:
        """Retorna resumo das transações no período."""
        totals = self.repository.get_totals_by_type(user_id, start_date, end_date)
        count = self.repository.count_by_user(user_id, start_date, end_date)
        
        expenses_by_cat = self.repository.get_totals_by_category(
            user_id, TransactionType.EXPENSE, start_date, end_date
        )
        income_by_cat = self.repository.get_totals_by_category(
            user_id, TransactionType.INCOME, start_date, end_date
        )
        
        return TransactionSummary(
            total_income=totals["income"],
            total_expense=totals["expense"],
            balance=totals["income"] - totals["expense"],
            transaction_count=count,
            expenses_by_category=expenses_by_cat,
            income_by_category=income_by_cat,
        )
    
    def get_cash_flow(
        self,
        user_id: UUID,
        start_date: date,
        end_date: date,
    ) -> dict:
        """Retorna fluxo de caixa do período."""
        daily_flow = self.repository.get_daily_flow(user_id, start_date, end_date)
        totals = self.repository.get_totals_by_type(user_id, start_date, end_date)
        
        return {
            "period_start": start_date,
            "period_end": end_date,
            "daily_flow": daily_flow,
            "total_income": totals["income"],
            "total_expense": totals["expense"],
            "net_flow": totals["income"] - totals["expense"],
        }
    
    def enrich_transaction(self, transaction: Transaction) -> dict:
        """Enriquece transação com dados relacionados."""
        data = {
            "id": transaction.id,
            "user_id": transaction.user_id,
            "account_id": transaction.account_id,
            "credit_card_id": transaction.credit_card_id,
            "category_id": transaction.category_id,
            "type": transaction.type,
            "description": transaction.description,
            "amount": transaction.amount,
            "date": transaction.date,
            "status": transaction.status,
            "is_recurring": transaction.is_recurring,
            "recurring_id": transaction.recurring_id,
            "notes": transaction.notes,
            "created_at": transaction.created_at,
            "updated_at": transaction.updated_at,
            "account_name": transaction.account.name if transaction.account else None,
            "credit_card_name": transaction.credit_card.name if transaction.credit_card else None,
            "category_name": transaction.category.name if transaction.category else None,
            "category_color": transaction.category.color if transaction.category else None,
        }
        return data
