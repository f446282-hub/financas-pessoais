import api from './api';
import { 
  Transaction, 
  TransactionCreate, 
  TransactionListResponse, 
  TransactionFilters,
  Category 
} from '@/types';

export const transactionsApi = {
  async getTransactions(filters?: TransactionFilters): Promise<TransactionListResponse> {
    const response = await api.get('/transactions', { params: filters });
    return response.data;
  },

  async getTransaction(id: string): Promise<Transaction> {
    const response = await api.get(`/transactions/${id}`);
    return response.data;
  },

  async createTransaction(data: TransactionCreate): Promise<Transaction> {
    const response = await api.post('/transactions', data);
    return response.data;
  },

  async updateTransaction(id: string, data: Partial<TransactionCreate>): Promise<Transaction> {
    const response = await api.put(`/transactions/${id}`, data);
    return response.data;
  },

  async deleteTransaction(id: string): Promise<void> {
    await api.delete(`/transactions/${id}`);
  },

  async getSummary(startDate?: string, endDate?: string) {
    const response = await api.get('/transactions/summary', {
      params: { start_date: startDate, end_date: endDate },
    });
    return response.data;
  },

  async getCashFlow(startDate: string, endDate: string) {
    const response = await api.get('/transactions/cash-flow', {
      params: { start_date: startDate, end_date: endDate },
    });
    return response.data;
  },

  // Categorias
  async getCategories(type?: 'income' | 'expense'): Promise<Category[]> {
    const response = await api.get('/categories', { params: { type } });
    return response.data;
  },

  async createCategory(data: { name: string; type: 'income' | 'expense'; icon?: string; color?: string }): Promise<Category> {
    const response = await api.post('/categories', data);
    return response.data;
  },
};
