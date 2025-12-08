import api from './api';
import { IndicatorValue } from '@/types';

export const indicatorsApi = {
  async getIndicators() {
    const response = await api.get('/indicators');
    return response.data;
  },

  async getIndicatorValues(startDate: string, endDate: string): Promise<{ indicators: IndicatorValue[]; period_start: string; period_end: string }> {
    const response = await api.get('/indicators/values', {
      params: { start_date: startDate, end_date: endDate },
    });
    return response.data;
  },
};
