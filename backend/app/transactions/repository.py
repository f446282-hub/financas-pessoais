"""
Repository de Transações e Categorias - Camada de acesso a dados.
"""

from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.transactions.models import Transaction, Category, TransactionType, TransactionStatus


class CategoryRepository:
    """Repository para operações de Categorias."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, category_id: UUID) -> Optional[Category]:
        """Busca categoria por ID."""
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def get_all_for_user(self, user_id: UUID) -> List[Category]:
        """Lista categorias disponíveis para o usuário."""
        return (
            self.db.query(Category)
            .filter(
                or_(
                    Category.user_id == None,
                    Category.user_id == user_id
                ),
                Category.is_active == True
            )
            .order_by(Category.type, Category.name)
            .all()
        )
    
    def get_by_type(self, user_id: UUID, tx_type: TransactionType) -> List[Category]:
        """Lista categorias de um tipo específico."""
        return (
            self.db.query(Category)
            .filter(
                or_(
                    Category.user_id == None,
                    Category.user_id == user_id
                ),
                Category.type == tx_type,
                Category.is_active == True
            )
            .order_by(Category.name)
            .all()
        )
    
    def create(self, category: Category) -> Category:
        """Cria nova categoria."""
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def create_default_categories(self) -> List[Category]:
        """Cria categorias padrão globais."""
        defaults = [
            # Despesas
            {"name": "Alimentação", "type": TransactionType.EXPENSE, "icon": "utensils", "color": "#EF4444"},
            {"name": "Transporte", "type": TransactionType.EXPENSE, "icon": "car", "color": "#F59E0B"},
            {"name": "Moradia", "type": TransactionType.EXPENSE, "icon": "home", "color": "#8B5CF6"},
            {"name": "Saúde", "type": TransactionType.EXPENSE, "icon": "heart", "color": "#EC4899"},
            {"name": "Educação", "type": TransactionType.EXPENSE, "icon": "book", "color": "#3B82F6"},
            {"name": "Lazer", "type": TransactionType.EXPENSE, "icon": "gamepad", "color": "#10B981"},
            {"name": "Compras", "type": TransactionType.EXPENSE, "icon": "shopping-bag", "color": "#F97316"},
            {"name": "Serviços", "type": TransactionType.EXPENSE, "icon": "wrench", "color": "#6366F1"},
            {"name": "Outros", "type": TransactionType.EXPENSE, "icon": "more-horizontal", "color": "#6B7280"},
            # Receitas
            {"name": "Salário", "type": TransactionType.INCOME, "icon": "briefcase", "color": "#22C55E"},
            {"name": "Freelance", "type": TransactionType.INCOME, "icon": "laptop", "color": "#14B8A6"},
            {"name": "Investimentos", "type": TransactionType.INCOME, "icon": "trending-up", "color": "#0EA5E9"},
            {"name": "Vendas", "type": TransactionType.INCOME, "icon": "tag", "color": "#A855F7"},
            {"name": "Outros", "type": TransactionType.INCOME, "icon": "plus-circle", "color": "#6B7280"},
        ]
        
        categories = []
        for data in defaults:
            category = Category(
                user_id=None,
                name=data["name"],
                type=data["type"],
                icon=data["icon"],
                color=data["color"],
            )
            self.db.add(category)
            categories.append(category)
        
        self.db.commit()
        return categories


class TransactionRepository:
    """Repository para operações de Transações."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, transaction_id: UUID, user_id: UUID) -> Optional[Transaction]:
        """Busca transação por ID."""
        return (
            self.db.query(Transaction)
            .filter(Transaction.id == transaction_id, Transaction.user_id == user_id)
            .first()
        )
    
    def get_all_by_user(
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
        """Lista transações do usuário com filtros."""
        query = self.db.query(Transaction).filter(Transaction.user_id == user_id)
        
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        if tx_type:
            query = query.filter(Transaction.type == tx_type)
        if status:
            query = query.filter(Transaction.status == status)
        if account_id:
            query = query.filter(Transaction.account_id == account_id)
        if credit_card_id:
            query = query.filter(Transaction.credit_card_id == credit_card_id)
        if category_id:
            query = query.filter(Transaction.category_id == category_id)
        
        return (
            query
            .order_by(Transaction.date.desc(), Transaction.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
    
    def count_by_user(
        self,
        user_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        tx_type: Optional[TransactionType] = None,
    ) -> int:
        """Conta transações do usuário."""
        query = self.db.query(func.count(Transaction.id)).filter(Transaction.user_id == user_id)
        
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        if tx_type:
            query = query.filter(Transaction.type == tx_type)
        
        return query.scalar() or 0
    
    def get_totals_by_type(
        self,
        user_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        account_id: Optional[UUID] = None,
    ) -> dict:
        """Calcula totais de receitas e despesas."""
        query = (
            self.db.query(
                Transaction.type,
                func.sum(Transaction.amount).label("total")
            )
            .filter(
                Transaction.user_id == user_id,
                Transaction.status != TransactionStatus.CANCELLED
            )
            .group_by(Transaction.type)
        )
        
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        if account_id:
            query = query.filter(Transaction.account_id == account_id)
        
        results = query.all()
        
        totals = {"income": Decimal("0.00"), "expense": Decimal("0.00")}
        for row in results:
            totals[row.type.value] = row.total or Decimal("0.00")
        
        return totals
    
    def get_totals_by_category(
        self,
        user_id: UUID,
        tx_type: TransactionType,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[dict]:
        """Calcula totais agrupados por categoria."""
        query = (
            self.db.query(
                Category.id,
                Category.name,
                Category.color,
                func.sum(Transaction.amount).label("total")
            )
            .join(Transaction, Transaction.category_id == Category.id)
            .filter(
                Transaction.user_id == user_id,
                Transaction.type == tx_type,
                Transaction.status != TransactionStatus.CANCELLED
            )
            .group_by(Category.id, Category.name, Category.color)
        )
        
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        
        results = query.order_by(func.sum(Transaction.amount).desc()).all()
        
        return [
            {
                "category_id": str(row.id),
                "category_name": row.name,
                "category_color": row.color,
                "total": row.total or Decimal("0.00"),
            }
            for row in results
        ]
    
    def get_daily_flow(
        self,
        user_id: UUID,
        start_date: date,
        end_date: date,
    ) -> List[dict]:
        """Calcula fluxo de caixa diário."""
        query = (
            self.db.query(
                Transaction.date,
                Transaction.type,
                func.sum(Transaction.amount).label("total")
            )
            .filter(
                Transaction.user_id == user_id,
                Transaction.date >= start_date,
                Transaction.date <= end_date,
                Transaction.status != TransactionStatus.CANCELLED
            )
            .group_by(Transaction.date, Transaction.type)
            .order_by(Transaction.date)
        )
        
        results = query.all()
        
        daily_data = {}
        for row in results:
            date_str = row.date.isoformat()
            if date_str not in daily_data:
                daily_data[date_str] = {"income": Decimal("0.00"), "expense": Decimal("0.00")}
            daily_data[date_str][row.type.value] = row.total or Decimal("0.00")
        
        return [
            {
                "date": d,
                "income": data["income"],
                "expense": data["expense"],
                "balance": data["income"] - data["expense"],
            }
            for d, data in sorted(daily_data.items())
        ]
    
    def calculate_account_balance(self, account_id: UUID) -> Decimal:
        """Calcula saldo da conta baseado nas transações."""
        income = (
            self.db.query(func.sum(Transaction.amount))
            .filter(
                Transaction.account_id == account_id,
                Transaction.type == TransactionType.INCOME,
                Transaction.status != TransactionStatus.CANCELLED
            )
            .scalar()
        ) or Decimal("0.00")
        
        expense = (
            self.db.query(func.sum(Transaction.amount))
            .filter(
                Transaction.account_id == account_id,
                Transaction.type == TransactionType.EXPENSE,
                Transaction.status != TransactionStatus.CANCELLED
            )
            .scalar()
        ) or Decimal("0.00")
        
        return income - expense
    
    def calculate_card_invoice(self, card_id: UUID) -> Decimal:
        """Calcula valor da fatura atual do cartão."""
        total = (
            self.db.query(func.sum(Transaction.amount))
            .filter(
                Transaction.credit_card_id == card_id,
                Transaction.type == TransactionType.EXPENSE,
                Transaction.status == TransactionStatus.PENDING
            )
            .scalar()
        )
        return total or Decimal("0.00")
    
    def create(self, transaction: Transaction) -> Transaction:
        """Cria nova transação."""
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction
    
    def update(self, transaction: Transaction) -> Transaction:
        """Atualiza transação existente."""
        self.db.commit()
        self.db.refresh(transaction)
        return transaction
    
    def delete(self, transaction: Transaction) -> None:
        """Remove transação do banco."""
        self.db.delete(transaction)
        self.db.commit()
