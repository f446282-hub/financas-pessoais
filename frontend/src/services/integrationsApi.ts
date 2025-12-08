import api from './api';
import { BankProvider, BankIntegration, WhatsAppSettings } from '@/types';

export const integrationsApi = {
  // Bancos
  async getBankProviders(): Promise<BankProvider[]> {
    const response = await api.get('/integrations/banks/providers');
    return response.data;
  },

  async getBankIntegrations(): Promise<BankIntegration[]> {
    const response = await api.get('/integrations/banks');
    return response.data;
  },

  async connectBank(provider: string): Promise<BankIntegration> {
    const response = await api.post(`/integrations/banks/${provider}/connect`);
    return response.data;
  },

  async disconnectBank(provider: string): Promise<void> {
    await api.post(`/integrations/banks/${provider}/disconnect`);
  },

  async syncBank(provider: string): Promise<BankIntegration> {
    const response = await api.post(`/integrations/banks/${provider}/sync`);
    return response.data;
  },

  // WhatsApp
  async getWhatsAppSettings(): Promise<WhatsAppSettings> {
    const response = await api.get('/integrations/whatsapp');
    return response.data;
  },

  async updateWhatsAppSettings(data: Partial<WhatsAppSettings>): Promise<WhatsAppSettings> {
    const response = await api.put('/integrations/whatsapp', data);
    return response.data;
  },
};
