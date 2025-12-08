// ===========================================
// User Types
// ===========================================

export interface User {
  id: string;
  email: string;
  name: string;
  avatar_url?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// ===========================================
// Account Types
// ===========================================

export type AccountType = 'checking' | 'savings' | 'wallet' | 'investment' | 'other';

export interface Account {
  id: string;
  user_id: string;
  name: string;
  type: AccountType;
  institution?: string;
  initial_balance: number;
  current_balance: number;
  color?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface AccountCreate {
  name: string;
  type: AccountType;
  institution?: string;
  initial_balance?: number;
  color?: string;
}

export interface AccountListResponse {
  accounts: Account[];
  total: number;
  total_balance: number;
}

// ===========================================
// Credit Card Types
// ===========================================

export interface CreditCard {
  id: string;
  user_id: string;
  name: string;
  institution: string;
  limit: number;
  closing_day: number;
  due_day: number;
  color?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  current_invoice?: number;
  available_limit?: number;
}

export interface CreditCardCreate {
  name: string;
  institution: string;
  limit: number;
  closing_day: number;
  due_day: number;
  color?: string;
}

export interface CreditCardListResponse {
  cards: CreditCard[];
  total: number;
  total_limit: number;
}

// ===========================================
// Transaction Types
// ===========================================

export type TransactionType = 'income' | 'expense';
export type TransactionStatus = 'pending' | 'paid' | 'cancelled';

export interface Transaction {
  id: string;
  user_id: string;
  account_id?: string;
  credit_card_id?: string;
  category_id?: string;
  type: TransactionType;
  description: string;
  amount: number;
  date: string;
  status: TransactionStatus;
  is_recurring: boolean;
  recurring_id?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
  account_name?: string;
  credit_card_name?: string;
  category_name?: string;
  category_color?: string;
}

export interface TransactionCreate {
  type: TransactionType;
  description: string;
  amount: number;
  date: string;
  status?: TransactionStatus;
  account_id?: string;
  credit_card_id?: string;
  category_id?: string;
  is_recurring?: boolean;
  notes?: string;
}

export interface TransactionListResponse {
  transactions: Transaction[];
  total: number;
  total_income: number;
  total_expense: number;
  balance: number;
}

export interface TransactionFilters {
  start_date?: string;
  end_date?: string;
  type?: TransactionType;
  status?: TransactionStatus;
  account_id?: string;
  credit_card_id?: string;
  category_id?: string;
}

// ===========================================
// Category Types
// ===========================================

export interface Category {
  id: string;
  user_id?: string;
  name: string;
  type: TransactionType;
  icon?: string;
  color?: string;
  is_active: boolean;
}

// ===========================================
// Dashboard Types
// ===========================================

export interface DashboardSummary {
  total_balance: number;
  total_income: number;
  total_expense: number;
  balance: number;
  income_committed_pct: number;
  account_count: number;
  transaction_count: number;
}

export interface CategoryBreakdown {
  category_id: string;
  category_name: string;
  category_color?: string;
  total: number;
  percentage: number;
}

export interface DailyCashFlow {
  date: string;
  income: number;
  expense: number;
  balance: number;
}

export interface MonthlyComparison {
  month: string;
  income: number;
  expense: number;
}

export interface DashboardData {
  summary: DashboardSummary;
  expenses_by_category: CategoryBreakdown[];
  income_by_category: CategoryBreakdown[];
  cash_flow: DailyCashFlow[];
  monthly_comparison: MonthlyComparison[];
}

// ===========================================
// Investment Types
// ===========================================

export interface InvestmentPortfolio {
  id: string;
  user_id: string;
  name: string;
  type?: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  total_invested?: number;
  current_balance?: number;
}

export interface InvestmentEntry {
  id: string;
  portfolio_id: string;
  type: 'deposit' | 'withdrawal';
  amount: number;
  date: string;
  description?: string;
  created_at: string;
}

// ===========================================
// Indicator Types
// ===========================================

export type IndicatorType = 'percentage' | 'currency' | 'number';

export interface IndicatorValue {
  code: string;
  name: string;
  value: number;
  type: IndicatorType;
  formatted_value: string;
}

// ===========================================
// Integration Types
// ===========================================

export type IntegrationStatus = 'disconnected' | 'connected' | 'error';

export interface BankProvider {
  code: string;
  name: string;
  logo_url?: string;
  available: boolean;
}

export interface BankIntegration {
  id: string;
  provider: string;
  status: IntegrationStatus;
  connected_at?: string;
  last_sync_at?: string;
}

export interface WhatsAppSettings {
  id?: string;
  phone_number?: string;
  is_active: boolean;
  alert_on_high_expense: boolean;
  high_expense_threshold?: number;
  daily_summary: boolean;
  weekly_summary: boolean;
}
