"""
Dashboard module - Agregações e dados consolidados para o dashboard.
"""

from datetime import date, timedelta
from decimal import Decimal
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import APIRouter, Query

from app.core.dependencies import CurrentUser, DatabaseSession
from app.transactions.repository import TransactionRepository
from app.transactions.models import TransactionType
from app.accounts.service import AccountService


# ===========================================
# Schemas
# ===========================================

class DashboardSummary(BaseModel):
    """Resumo principal do dashboard."""
    total_balance: Decimal
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal
    income_committed_pct: Decimal
    account_count: int
    transaction_count: int


class CategoryBreakdown(BaseModel):
    """Distribuição por categoria."""
    category_id: str
    category_name: str
    category_color: Optional[str]
    total: Decimal
    percentage: Decimal


class DailyCashFlowItem(BaseModel):
    """Item do fluxo de caixa diário."""
    date: str
    income: Decimal
    expense: Decimal
    balance: Decimal


class MonthlyComparison(BaseModel):
    """Comparação mensal."""
    month: str
    income: Decimal
    expense: Decimal


class DashboardData(BaseModel):
    """Dados completos do dashboard."""
    summary: DashboardSummary
    expenses_by_category: List[CategoryBreakdown]
    income_by_category: List[CategoryBreakdown]
    cash_flow: List[DailyCashFlowItem]
    monthly_comparison: List[MonthlyComparison]


# ===========================================
# Service
# ===========================================

class DashboardService:
    """Serviço de agregação de dados para o dashboard."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_summary(
        self, 
        user_id: UUID, 
        start_date: date, 
        end_date: date
    ) -> DashboardSummary:
        """Calcula resumo do período."""
        tx_repo = TransactionRepository(self.db)
        account_service = AccountService(self.db)
        
        # Totais de transações
        totals = tx_repo.get_totals_by_type(user_id, start_date, end_date)
        income = totals["income"]
        expense = totals["expense"]
        
        # Saldo total das contas
        total_balance = account_service.get_total_balance(user_id)
        
        # Quantidade de contas e transações
        accounts = account_service.get_all(user_id)
        tx_count = tx_repo.count_by_user(user_id, start_date, end_date)
        
        # % Renda comprometida
        committed_pct = (expense / income * 100) if income > 0 else Decimal("0")
        
        return DashboardSummary(
            total_balance=total_balance,
            total_income=income,
            total_expense=expense,
            balance=income - expense,
            income_committed_pct=committed_pct.quantize(Decimal("0.01")),
            account_count=len(accounts),
            transaction_count=tx_count,
        )
    
    def get_expenses_by_category(
        self, 
        user_id: UUID, 
        start_date: date, 
        end_date: date
    ) -> List[CategoryBreakdown]:
        """Retorna distribuição de despesas por categoria."""
        tx_repo = TransactionRepository(self.db)
        data = tx_repo.get_totals_by_category(user_id, TransactionType.EXPENSE, start_date, end_date)
        
        total = sum(item["total"] for item in data)
        
        return [
            CategoryBreakdown(
                category_id=item["category_id"],
                category_name=item["category_name"],
                category_color=item["category_color"],
                total=item["total"],
                percentage=(item["total"] / total * 100).quantize(Decimal("0.01")) if total > 0 else Decimal("0"),
            )
            for item in data
        ]
    
    def get_income_by_category(
        self, 
        user_id: UUID, 
        start_date: date, 
        end_date: date
    ) -> List[CategoryBreakdown]:
        """Retorna distribuição de receitas por categoria."""
        tx_repo = TransactionRepository(self.db)
        data = tx_repo.get_totals_by_category(user_id, TransactionType.INCOME, start_date, end_date)
        
        total = sum(item["total"] for item in data)
        
        return [
            CategoryBreakdown(
                category_id=item["category_id"],
                category_name=item["category_name"],
                category_color=item["category_color"],
                total=item["total"],
                percentage=(item["total"] / total * 100).quantize(Decimal("0.01")) if total > 0 else Decimal("0"),
            )
            for item in data
        ]
    
    def get_cash_flow(
        self, 
        user_id: UUID, 
        start_date: date, 
        end_date: date
    ) -> List[DailyCashFlowItem]:
        """Retorna fluxo de caixa diário."""
        tx_repo = TransactionRepository(self.db)
        data = tx_repo.get_daily_flow(user_id, start_date, end_date)
        
        return [
            DailyCashFlowItem(
                date=item["date"],
                income=item["income"],
                expense=item["expense"],
                balance=item["balance"],
            )
            for item in data
        ]
    
    def get_monthly_comparison(
        self, 
        user_id: UUID, 
        months: int = 6
    ) -> List[MonthlyComparison]:
        """Retorna comparação mensal dos últimos N meses."""
        tx_repo = TransactionRepository(self.db)
        results = []
        
        today = date.today()
        
        for i in range(months - 1, -1, -1):
            # Calcular primeiro e último dia do mês
            month_date = today.replace(day=1) - timedelta(days=i * 30)
            month_start = month_date.replace(day=1)
            
            # Último dia do mês
            if month_start.month == 12:
                month_end = month_start.replace(year=month_start.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                month_end = month_start.replace(month=month_start.month + 1, day=1) - timedelta(days=1)
            
            totals = tx_repo.get_totals_by_type(user_id, month_start, month_end)
            
            results.append(MonthlyComparison(
                month=month_start.strftime("%Y-%m"),
                income=totals["income"],
                expense=totals["expense"],
            ))
        
        return results
    
    def get_full_dashboard(
        self, 
        user_id: UUID, 
        start_date: date, 
        end_date: date
    ) -> DashboardData:
        """Retorna todos os dados do dashboard."""
        return DashboardData(
            summary=self.get_summary(user_id, start_date, end_date),
            expenses_by_category=self.get_expenses_by_category(user_id, start_date, end_date),
            income_by_category=self.get_income_by_category(user_id, start_date, end_date),
            cash_flow=self.get_cash_flow(user_id, start_date, end_date),
            monthly_comparison=self.get_monthly_comparison(user_id),
        )


# ===========================================
# Router
# ===========================================

dashboard_router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@dashboard_router.get("/summary", response_model=DashboardSummary)
async def get_summary(
    current_user: CurrentUser,
    db: DatabaseSession,
    start_date: date = Query(...),
    end_date: date = Query(...),
):
    """Retorna resumo do período para os cards principais."""
    service = DashboardService(db)
    return service.get_summary(current_user.id, start_date, end_date)


@dashboard_router.get("/expenses-by-category", response_model=List[CategoryBreakdown])
async def get_expenses_by_category(
    current_user: CurrentUser,
    db: DatabaseSession,
    start_date: date = Query(...),
    end_date: date = Query(...),
):
    """Retorna distribuição de despesas por categoria."""
    service = DashboardService(db)
    return service.get_expenses_by_category(current_user.id, start_date, end_date)


@dashboard_router.get("/income-by-category", response_model=List[CategoryBreakdown])
async def get_income_by_category(
    current_user: CurrentUser,
    db: DatabaseSession,
    start_date: date = Query(...),
    end_date: date = Query(...),
):
    """Retorna distribuição de receitas por categoria."""
    service = DashboardService(db)
    return service.get_income_by_category(current_user.id, start_date, end_date)


@dashboard_router.get("/cash-flow", response_model=List[DailyCashFlowItem])
async def get_cash_flow(
    current_user: CurrentUser,
    db: DatabaseSession,
    start_date: date = Query(...),
    end_date: date = Query(...),
):
    """Retorna fluxo de caixa diário do período."""
    service = DashboardService(db)
    return service.get_cash_flow(current_user.id, start_date, end_date)


@dashboard_router.get("/monthly-comparison", response_model=List[MonthlyComparison])
async def get_monthly_comparison(
    current_user: CurrentUser,
    db: DatabaseSession,
    months: int = Query(6, ge=1, le=12),
):
    """Retorna comparação dos últimos N meses."""
    service = DashboardService(db)
    return service.get_monthly_comparison(current_user.id, months)


@dashboard_router.get("", response_model=DashboardData)
async def get_full_dashboard(
    current_user: CurrentUser,
    db: DatabaseSession,
    start_date: date = Query(...),
    end_date: date = Query(...),
):
    """Retorna todos os dados do dashboard em uma única chamada."""
    service = DashboardService(db)
    return service.get_full_dashboard(current_user.id, start_date, end_date)
