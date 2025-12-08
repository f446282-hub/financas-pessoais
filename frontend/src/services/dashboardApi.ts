import api from './api';
import { DashboardData, DashboardSummary, CategoryBreakdown, DailyCashFlow, MonthlyComparison } from '@/types';

export const dashboardApi = {
  async getFullDashboard(startDate: string, endDate: string): Promise<DashboardData> {
    const response = await api.get('/dashboard', {
      params: { start_date: startDate, end_date: endDate },
    });
    return response.data;
  },

  async getSummary(startDate: string, endDate: string): Promise<DashboardSummary> {
    const response = await api.get('/dashboard/summary', {
      params: { start_date: startDate, end_date: endDate },
    });
    return response.data;
  },

  async getExpensesByCategory(startDate: string, endDate: string): Promise<CategoryBreakdown[]> {
    const response = await api.get('/dashboard/expenses-by-category', {
      params: { start_date: startDate, end_date: endDate },
    });
    return response.data;
  },

  async getIncomeByCategory(startDate: string, endDate: string): Promise<CategoryBreakdown[]> {
    const response = await api.get('/dashboard/income-by-category', {
      params: { start_date: startDate, end_date: endDate },
    });
    return response.data;
  },

  async getCashFlow(startDate: string, endDate: string): Promise<DailyCashFlow[]> {
    const response = await api.get('/dashboard/cash-flow', {
      params: { start_date: startDate, end_date: endDate },
    });
    return response.data;
  },

  async getMonthlyComparison(months = 6): Promise<MonthlyComparison[]> {
    const response = await api.get('/dashboard/monthly-comparison', {
      params: { months },
    });
    return response.data;
  },
};
