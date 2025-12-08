'use client';

import { useEffect, useState } from 'react';
import { AppLayout } from '@/components/layout';
import { Card, CardHeader } from '@/components/ui';
import {
  CashFlowLineChart,
  MonthlyComparisonBarChart,
  ExpensesPieChart,
} from '@/components/charts';
import { dashboardApi } from '@/services';
import { DashboardData } from '@/types';
import { formatCurrency, formatPercent, getFirstDayOfMonth, getLastDayOfMonth } from '@/utils/formatters';
import {
  Wallet,
  TrendingUp,
  TrendingDown,
  PiggyBank,
  ArrowUpRight,
  ArrowDownRight,
  RefreshCw,
} from 'lucide-react';

// Card de Resumo
interface SummaryCardProps {
  title: string;
  value: string;
  change?: number;
  icon: React.ReactNode;
  color: 'green' | 'red' | 'blue' | 'purple';
}

function SummaryCard({ title, value, change, icon, color }: SummaryCardProps) {
  const colorClasses = {
    green: 'bg-green-50 text-green-700',
    red: 'bg-red-50 text-red-700',
    blue: 'bg-blue-50 text-blue-700',
    purple: 'bg-purple-50 text-purple-700',
  };

  return (
    <Card className="card-hover">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="mt-2 text-2xl font-bold text-gray-800">{value}</p>
          {change !== undefined && (
            <div className="mt-2 flex items-center gap-1">
              {change >= 0 ? (
                <ArrowUpRight className="h-4 w-4 text-green-600" />
              ) : (
                <ArrowDownRight className="h-4 w-4 text-red-600" />
              )}
              <span className={change >= 0 ? 'text-sm text-green-600' : 'text-sm text-red-600'}>
                {formatPercent(Math.abs(change))}
              </span>
              <span className="text-sm text-gray-400">vs mês anterior</span>
            </div>
          )}
        </div>
        <div className={`rounded-xl p-3 ${colorClasses[color]}`}>{icon}</div>
      </div>
    </Card>
  );
}

// Estado de Loading
function LoadingState() {
  return (
    <div className="flex h-64 items-center justify-center">
      <div className="h-12 w-12 spinner" />
    </div>
  );
}

// Estado sem dados
function EmptyState({ message }: { message: string }) {
  return (
    <div className="flex h-64 flex-col items-center justify-center text-gray-400">
      <PiggyBank className="mb-4 h-12 w-12" />
      <p>{message}</p>
    </div>
  );
}

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState({
    start: getFirstDayOfMonth(),
    end: getLastDayOfMonth(),
  });

  const fetchData = async () => {
    try {
      setLoading(true);
      const result = await dashboardApi.getFullDashboard(period.start, period.end);
      setData(result);
    } catch (error) {
      console.error('Erro ao carregar dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [period]);

  return (
    <AppLayout title="Dashboard">
      {/* Filtros */}
      <div className="mb-6 flex items-center justify-between">
        <div className="flex gap-2">
          <select
            className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm"
            onChange={(e) => {
              const today = new Date();
              let start: Date;
              let end: Date = new Date(today.getFullYear(), today.getMonth() + 1, 0);

              switch (e.target.value) {
                case 'current':
                  start = new Date(today.getFullYear(), today.getMonth(), 1);
                  break;
                case 'last':
                  start = new Date(today.getFullYear(), today.getMonth() - 1, 1);
                  end = new Date(today.getFullYear(), today.getMonth(), 0);
                  break;
                case 'last3':
                  start = new Date(today.getFullYear(), today.getMonth() - 2, 1);
                  break;
                default:
                  start = new Date(today.getFullYear(), today.getMonth(), 1);
              }

              setPeriod({
                start: start.toISOString().split('T')[0],
                end: end.toISOString().split('T')[0],
              });
            }}
          >
            <option value="current">Mês atual</option>
            <option value="last">Mês anterior</option>
            <option value="last3">Últimos 3 meses</option>
          </select>
        </div>
        <button
          onClick={fetchData}
          className="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-600 hover:bg-gray-50"
        >
          <RefreshCw className="h-4 w-4" />
          Atualizar
        </button>
      </div>

      {loading ? (
        <LoadingState />
      ) : !data ? (
        <EmptyState message="Nenhum dado encontrado" />
      ) : (
        <>
          {/* Cards de Resumo */}
          <div className="mb-6 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            <SummaryCard
              title="Saldo Total"
              value={formatCurrency(data.summary.total_balance)}
              icon={<Wallet className="h-6 w-6" />}
              color="blue"
            />
            <SummaryCard
              title="Receitas do Mês"
              value={formatCurrency(data.summary.total_income)}
              icon={<TrendingUp className="h-6 w-6" />}
              color="green"
            />
            <SummaryCard
              title="Despesas do Mês"
              value={formatCurrency(data.summary.total_expense)}
              icon={<TrendingDown className="h-6 w-6" />}
              color="red"
            />
            <SummaryCard
              title="% Renda Comprometida"
              value={formatPercent(data.summary.income_committed_pct)}
              icon={<PiggyBank className="h-6 w-6" />}
              color="purple"
            />
          </div>

          {/* Gráficos */}
          <div className="grid gap-6 lg:grid-cols-2">
            {/* Fluxo de Caixa */}
            <Card>
              <CardHeader title="Fluxo de Caixa" subtitle="Receitas e despesas diárias" />
              {data.cash_flow.length > 0 ? (
                <CashFlowLineChart data={data.cash_flow} />
              ) : (
                <EmptyState message="Nenhuma movimentação no período" />
              )}
            </Card>

            {/* Despesas por Categoria */}
            <Card>
              <CardHeader title="Despesas por Categoria" subtitle="Distribuição das despesas" />
              {data.expenses_by_category.length > 0 ? (
                <ExpensesPieChart data={data.expenses_by_category} />
              ) : (
                <EmptyState message="Nenhuma despesa no período" />
              )}
            </Card>

            {/* Comparação Mensal */}
            <Card className="lg:col-span-2">
              <CardHeader title="Comparação Mensal" subtitle="Receitas vs Despesas nos últimos 6 meses" />
              {data.monthly_comparison.length > 0 ? (
                <MonthlyComparisonBarChart data={data.monthly_comparison} height={350} />
              ) : (
                <EmptyState message="Nenhum dado para comparação" />
              )}
            </Card>
          </div>

          {/* Lista de categorias */}
          {data.expenses_by_category.length > 0 && (
            <Card className="mt-6">
              <CardHeader title="Top Categorias de Despesa" />
              <div className="space-y-3">
                {data.expenses_by_category.slice(0, 5).map((cat, index) => (
                  <div key={index} className="flex items-center gap-4">
                    <div
                      className="h-3 w-3 rounded-full"
                      style={{ backgroundColor: cat.category_color || '#6b7280' }}
                    />
                    <div className="flex-1">
                      <div className="flex justify-between">
                        <span className="text-sm font-medium text-gray-700">{cat.category_name}</span>
                        <span className="text-sm text-gray-500">{formatCurrency(cat.total)}</span>
                      </div>
                      <div className="mt-1 h-2 w-full rounded-full bg-gray-100">
                        <div
                          className="h-2 rounded-full"
                          style={{
                            width: `${cat.percentage}%`,
                            backgroundColor: cat.category_color || '#6b7280',
                          }}
                        />
                      </div>
                    </div>
                    <span className="text-sm font-medium text-gray-500">{cat.percentage.toFixed(0)}%</span>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </>
      )}
    </AppLayout>
  );
}
