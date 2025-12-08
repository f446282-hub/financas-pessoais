import api from './api';
import { Account, AccountCreate, AccountListResponse, CreditCard, CreditCardCreate, CreditCardListResponse } from '@/types';

export const accountsApi = {
  // Contas
  async getAccounts(includeInactive = false): Promise<AccountListResponse> {
    const response = await api.get('/accounts', {
      params: { include_inactive: includeInactive },
    });
    return response.data;
  },

  async getAccount(id: string): Promise<Account> {
    const response = await api.get(`/accounts/${id}`);
    return response.data;
  },

  async createAccount(data: AccountCreate): Promise<Account> {
    const response = await api.post('/accounts', data);
    return response.data;
  },

  async updateAccount(id: string, data: Partial<AccountCreate>): Promise<Account> {
    const response = await api.put(`/accounts/${id}`, data);
    return response.data;
  },

  async deleteAccount(id: string): Promise<void> {
    await api.delete(`/accounts/${id}`);
  },

  // Cartões de Crédito
  async getCreditCards(includeInactive = false): Promise<CreditCardListResponse> {
    const response = await api.get('/credit-cards', {
      params: { include_inactive: includeInactive },
    });
    return response.data;
  },

  async getCreditCard(id: string): Promise<CreditCard> {
    const response = await api.get(`/credit-cards/${id}`);
    return response.data;
  },

  async createCreditCard(data: CreditCardCreate): Promise<CreditCard> {
    const response = await api.post('/credit-cards', data);
    return response.data;
  },

  async updateCreditCard(id: string, data: Partial<CreditCardCreate>): Promise<CreditCard> {
    const response = await api.put(`/credit-cards/${id}`, data);
    return response.data;
  },

  async deleteCreditCard(id: string): Promise<void> {
    await api.delete(`/credit-cards/${id}`);
  },
};
