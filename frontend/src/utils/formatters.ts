import { format, parseISO } from 'date-fns';
import { ptBR } from 'date-fns/locale';

// Formatação de moeda
export function formatCurrency(value: number): string {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(value);
}

// Formatação de percentual
export function formatPercent(value: number): string {
  return `${value.toFixed(1)}%`;
}

// Formatação de data
export function formatDate(date: string | Date, pattern = 'dd/MM/yyyy'): string {
  const d = typeof date === 'string' ? parseISO(date) : date;
  return format(d, pattern, { locale: ptBR });
}

// Formatação de data e hora
export function formatDateTime(date: string | Date): string {
  const d = typeof date === 'string' ? parseISO(date) : date;
  return format(d, "dd/MM/yyyy 'às' HH:mm", { locale: ptBR });
}

// Formatação de mês
export function formatMonth(date: string): string {
  return format(parseISO(date + '-01'), 'MMM/yy', { locale: ptBR });
}

// Data atual formatada para inputs
export function getCurrentDate(): string {
  return format(new Date(), 'yyyy-MM-dd');
}

// Primeiro dia do mês
export function getFirstDayOfMonth(): string {
  const today = new Date();
  return format(new Date(today.getFullYear(), today.getMonth(), 1), 'yyyy-MM-dd');
}

// Último dia do mês
export function getLastDayOfMonth(): string {
  const today = new Date();
  return format(new Date(today.getFullYear(), today.getMonth() + 1, 0), 'yyyy-MM-dd');
}

// Tipo de conta formatado
export function formatAccountType(type: string): string {
  const types: Record<string, string> = {
    checking: 'Conta Corrente',
    savings: 'Poupança',
    wallet: 'Carteira',
    investment: 'Investimento',
    other: 'Outra',
  };
  return types[type] || type;
}

// Status da transação formatado
export function formatTransactionStatus(status: string): string {
  const statuses: Record<string, string> = {
    pending: 'Pendente',
    paid: 'Pago',
    cancelled: 'Cancelado',
  };
  return statuses[status] || status;
}

// Tipo de transação formatado
export function formatTransactionType(type: string): string {
  return type === 'income' ? 'Receita' : 'Despesa';
}

// Cores por tipo
export function getTypeColor(type: string): string {
  return type === 'income' ? '#22c55e' : '#ef4444';
}

// Truncar texto
export function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
}
