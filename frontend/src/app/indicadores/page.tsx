'use client';

import { useEffect, useState } from 'react';
import { AppLayout } from '@/components/layout';
import { Card, CardHeader } from '@/components/ui';
import { indicatorsApi } from '@/services';
import { IndicatorValue } from '@/types';
import { getFirstDayOfMonth, getLastDayOfMonth } from '@/utils/formatters';
import { Target, TrendingUp, TrendingDown, DollarSign, Percent, Hash, ArrowUpRight, ArrowDownRight } from 'lucide-react';

interface IndicatorCardProps {
  indicator: IndicatorValue;
}

function IndicatorCard({ indicator }: IndicatorCardProps) {
  const getIcon = () => {
    switch (indicator.type) {
      case 'percentage':
        return <Percent className="h-6 w-6" />;
      case 'currency':
        return <DollarSign className="h-6 w-6" />;
      default:
        return <Hash className="h-6 w-6" />;
    }
  };

  const getColorClass = () => {
    if (indicator.code === 'income_committed_pct') {
      return indicator.value > 80 ? 'text-red-600 bg-red-50' : indicator.value > 50 ? 'text-yellow-600 bg-yellow-50' : 'text-green-600 bg-green-50';
    }
    if (indicator.code === 'monthly_savings') {
      return indicator.value >= 0 ? 'text-green-600 bg-green-50' : 'text-red-600 bg-red-50';
    }
    return 'text-primary-600 bg-primary-50';
  };

  const getTrend = () => {
    if (indicator.code === 'income_committed_pct') {
      return indicator.value > 80 ? 'danger' : indicator.value > 50 ? 'warning' : 'success';
    }
    if (indicator.code === 'monthly_savings') {
      return indicator.value >= 0 ? 'success' : 'danger';
    }
    return 'neutral';
  };

  const trend = getTrend();

  return (
    <Card className="card-hover">
      <div className="flex items-start justify-between">
        <div className={`rounded-xl p-3 ${getColorClass()}`}>
          {getIcon()}
        </div>
        {trend !== 'neutral' && (
          <div className={`flex items-center gap-1 rounded-full px-2 py-1 text-xs font-medium ${
            trend === 'success' ? 'bg-green-100 text-green-700' :
            trend === 'warning' ? 'bg-yellow-100 text-yellow-700' :
            'bg-red-100 text-red-700'
          }`}>
            {trend === 'success' ? <ArrowUpRight className="h-3 w-3" /> : <ArrowDownRight className="h-3 w-3" />}
            {trend === 'success' ? 'Bom' : trend === 'warning' ? 'Atenção' : 'Crítico'}
          </div>
        )}
      </div>
      <div className="mt-4">
        <p className="text-sm text-gray-500">{indicator.name}</p>
        <p className="mt-1 text-3xl font-bold text-gray-800">{indicator.formatted_value}</p>
      </div>
      {/* Barra de progresso para percentuais */}
      {indicator.type === 'percentage' && (
        <div className="mt-4">
          <div className="h-2 w-full rounded-full bg-gray-100">
            <div
              className={`h-2 rounded-full transition-all ${
                trend === 'success' ? 'bg-green-500' :
                trend === 'warning' ? 'bg-yellow-500' :
                'bg-red-500'
              }`}
              style={{ width: `${Math.min(indicator.value, 100)}%` }}
            />
          </div>
        </div>
      )}
    </Card>
  );
}

export default function IndicadoresPage() {
  const [indicators, setIndicators] = useState<IndicatorValue[]>([]);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState({
    start: getFirstDayOfMonth(),
    end: getLastDayOfMonth(),
  });

  const fetchIndicators = async () => {
    try {
      setLoading(true);
      const data = await indicatorsApi.getIndicatorValues(period.start, period.end);
      setIndicators(data.indicators);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchIndicators();
  }, [period]);

  return (
    <AppLayout title="Indicadores">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <p className="text-gray-500">Acompanhe sua saúde financeira</p>
        </div>
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

      {/* Indicadores */}
      {loading ? (
        <div className="flex h-64 items-center justify-center">
          <div className="h-12 w-12 spinner" />
        </div>
      ) : indicators.length === 0 ? (
        <Card className="flex h-64 flex-col items-center justify-center text-gray-400">
          <Target className="mb-4 h-12 w-12" />
          <p>Nenhum indicador disponível</p>
          <p className="text-sm">Adicione transações para ver seus indicadores</p>
        </Card>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {indicators.map((indicator) => (
            <IndicatorCard key={indicator.code} indicator={indicator} />
          ))}
        </div>
      )}

      {/* Explicação dos indicadores */}
      <Card className="mt-8">
        <CardHeader title="Sobre os Indicadores" />
        <div className="space-y-4 text-sm text-gray-600">
          <div className="flex items-start gap-3">
            <div className="rounded-full bg-primary-100 p-2">
              <Percent className="h-4 w-4 text-primary-700" />
            </div>
            <div>
              <p className="font-semibold text-gray-800">% Renda Comprometida</p>
              <p>Quanto da sua renda está sendo gasto com despesas. Ideal: abaixo de 70%.</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="rounded-full bg-green-100 p-2">
              <TrendingUp className="h-4 w-4 text-green-700" />
            </div>
            <div>
              <p className="font-semibold text-gray-800">% Renda Disponível</p>
              <p>Quanto da sua renda sobra após as despesas. Esse valor pode ser investido!</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="rounded-full bg-blue-100 p-2">
              <DollarSign className="h-4 w-4 text-blue-700" />
            </div>
            <div>
              <p className="font-semibold text-gray-800">Saldo do Período</p>
              <p>Diferença entre receitas e despesas no período selecionado.</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="rounded-full bg-purple-100 p-2">
              <Hash className="h-4 w-4 text-purple-700" />
            </div>
            <div>
              <p className="font-semibold text-gray-800">Quantidade de Despesas</p>
              <p>Total de lançamentos de despesa no período.</p>
            </div>
          </div>
        </div>
      </Card>
    </AppLayout>
  );
}
