import api from './api';
import { InvestmentPortfolio, InvestmentEntry } from '@/types';

export const investmentsApi = {
  async getPortfolios(includeInactive = false): Promise<InvestmentPortfolio[]> {
    const response = await api.get('/investments/portfolios', {
      params: { include_inactive: includeInactive },
    });
    return response.data;
  },

  async getPortfolio(id: string): Promise<InvestmentPortfolio> {
    const response = await api.get(`/investments/portfolios/${id}`);
    return response.data;
  },

  async createPortfolio(data: { name: string; type?: string; description?: string }): Promise<InvestmentPortfolio> {
    const response = await api.post('/investments/portfolios', data);
    return response.data;
  },

  async updatePortfolio(id: string, data: Partial<{ name: string; type?: string; description?: string; is_active?: boolean }>): Promise<InvestmentPortfolio> {
    const response = await api.put(`/investments/portfolios/${id}`, data);
    return response.data;
  },

  async deletePortfolio(id: string): Promise<void> {
    await api.delete(`/investments/portfolios/${id}`);
  },

  async getEntries(portfolioId: string): Promise<InvestmentEntry[]> {
    const response = await api.get(`/investments/portfolios/${portfolioId}/entries`);
    return response.data;
  },

  async createEntry(portfolioId: string, data: { type: 'deposit' | 'withdrawal'; amount: number; date: string; description?: string }): Promise<InvestmentEntry> {
    const response = await api.post(`/investments/portfolios/${portfolioId}/entries`, data);
    return response.data;
  },
};
