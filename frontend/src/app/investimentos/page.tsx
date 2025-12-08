'use client';

import { useEffect, useState } from 'react';
import { AppLayout } from '@/components/layout';
import { Card, CardHeader, Button, Input, Modal, Badge } from '@/components/ui';
import { InvestmentAreaChart } from '@/components/charts';
import { investmentsApi, getErrorMessage } from '@/services';
import { InvestmentPortfolio, InvestmentEntry } from '@/types';
import { formatCurrency, formatDate } from '@/utils/formatters';
import { Plus, PiggyBank, TrendingUp, ArrowUpRight, ArrowDownRight, Trash2 } from 'lucide-react';

export default function InvestimentosPage() {
  const [portfolios, setPortfolios] = useState<InvestmentPortfolio[]>([]);
  const [loading, setLoading] = useState(true);
  const [isPortfolioModalOpen, setIsPortfolioModalOpen] = useState(false);
  const [isEntryModalOpen, setIsEntryModalOpen] = useState(false);
  const [selectedPortfolio, setSelectedPortfolio] = useState<InvestmentPortfolio | null>(null);
  const [entries, setEntries] = useState<InvestmentEntry[]>([]);
  const [formLoading, setFormLoading] = useState(false);
  const [error, setError] = useState('');

  const [portfolioForm, setPortfolioForm] = useState({ name: '', type: '', description: '' });
  const [entryForm, setEntryForm] = useState({ type: 'deposit' as 'deposit' | 'withdrawal', amount: 0, date: '', description: '' });

  const fetchPortfolios = async () => {
    try {
      setLoading(true);
      const data = await investmentsApi.getPortfolios();
      setPortfolios(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchEntries = async (portfolioId: string) => {
    try {
      const data = await investmentsApi.getEntries(portfolioId);
      setEntries(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchPortfolios();
  }, []);

  const handleCreatePortfolio = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setFormLoading(true);
    try {
      await investmentsApi.createPortfolio(portfolioForm);
      setIsPortfolioModalOpen(false);
      setPortfolioForm({ name: '', type: '', description: '' });
      fetchPortfolios();
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setFormLoading(false);
    }
  };

  const handleCreateEntry = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedPortfolio) return;
    setError('');
    setFormLoading(true);
    try {
      await investmentsApi.createEntry(selectedPortfolio.id, entryForm);
      setIsEntryModalOpen(false);
      setEntryForm({ type: 'deposit', amount: 0, date: '', description: '' });
      fetchPortfolios();
      fetchEntries(selectedPortfolio.id);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setFormLoading(false);
    }
  };

  const handleSelectPortfolio = (portfolio: InvestmentPortfolio) => {
    setSelectedPortfolio(portfolio);
    fetchEntries(portfolio.id);
  };

  const totalInvested = portfolios.reduce((sum, p) => sum + (p.total_invested || 0), 0);
  const totalBalance = portfolios.reduce((sum, p) => sum + (p.current_balance || 0), 0);

  // Mock data para o gráfico
  const chartData = entries.map((e, i) => ({
    date: e.date,
    value: entries.slice(0, i + 1).reduce((sum, en) => sum + (en.type === 'deposit' ? en.amount : -en.amount), 0),
  }));

  return (
    <AppLayout title="Investimentos">
      {/* Resumo */}
      <div className="mb-6 grid gap-6 md:grid-cols-3">
        <Card className="bg-gradient-to-br from-primary-700 to-primary-800 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-primary-200">Total Investido</p>
              <p className="mt-2 text-3xl font-bold">{formatCurrency(totalInvested)}</p>
            </div>
            <div className="rounded-xl bg-white/10 p-4">
              <PiggyBank className="h-8 w-8" />
            </div>
          </div>
        </Card>
        <Card className="bg-gradient-to-br from-green-600 to-green-700 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-green-200">Saldo Atual</p>
              <p className="mt-2 text-3xl font-bold">{formatCurrency(totalBalance)}</p>
            </div>
            <div className="rounded-xl bg-white/10 p-4">
              <TrendingUp className="h-8 w-8" />
            </div>
          </div>
        </Card>
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Carteiras</p>
              <p className="mt-2 text-3xl font-bold text-gray-800">{portfolios.length}</p>
            </div>
            <Button leftIcon={<Plus className="h-4 w-4" />} onClick={() => setIsPortfolioModalOpen(true)}>
              Nova Carteira
            </Button>
          </div>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Lista de Carteiras */}
        <Card className="lg:col-span-1">
          <CardHeader title="Carteiras" />
          {loading ? (
            <div className="flex h-32 items-center justify-center">
              <div className="h-8 w-8 spinner" />
            </div>
          ) : portfolios.length === 0 ? (
            <div className="flex h-32 flex-col items-center justify-center text-gray-400">
              <PiggyBank className="mb-2 h-8 w-8" />
              <p>Nenhuma carteira</p>
            </div>
          ) : (
            <div className="space-y-3">
              {portfolios.map((portfolio) => (
                <button
                  key={portfolio.id}
                  onClick={() => handleSelectPortfolio(portfolio)}
                  className={`w-full rounded-lg border p-4 text-left transition-all ${selectedPortfolio?.id === portfolio.id ? 'border-primary-500 bg-primary-50' : 'border-gray-200 hover:border-gray-300'}`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-semibold text-gray-800">{portfolio.name}</p>
                      <p className="text-sm text-gray-500">{portfolio.type || 'Geral'}</p>
                    </div>
                    <p className="font-bold text-green-600">{formatCurrency(portfolio.current_balance || 0)}</p>
                  </div>
                </button>
              ))}
            </div>
          )}
        </Card>

        {/* Detalhes da Carteira */}
        <Card className="lg:col-span-2">
          {selectedPortfolio ? (
            <>
              <CardHeader
                title={selectedPortfolio.name}
                subtitle={selectedPortfolio.type || 'Carteira Geral'}
                action={
                  <Button size="sm" leftIcon={<Plus className="h-4 w-4" />} onClick={() => setIsEntryModalOpen(true)}>
                    Registrar Movimentação
                  </Button>
                }
              />

              {/* Gráfico */}
              {chartData.length > 0 && (
                <div className="mb-6">
                  <InvestmentAreaChart data={chartData} height={200} />
                </div>
              )}

              {/* Lista de Movimentações */}
              <div className="space-y-2">
                <p className="text-sm font-semibold text-gray-500">Movimentações</p>
                {entries.length === 0 ? (
                  <p className="py-8 text-center text-gray-400">Nenhuma movimentação registrada</p>
                ) : (
                  <div className="max-h-64 space-y-2 overflow-y-auto">
                    {entries.map((entry) => (
                      <div key={entry.id} className="flex items-center justify-between rounded-lg border border-gray-100 bg-gray-50 p-3">
                        <div className="flex items-center gap-3">
                          <div className={`rounded-full p-2 ${entry.type === 'deposit' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'}`}>
                            {entry.type === 'deposit' ? <ArrowUpRight className="h-4 w-4" /> : <ArrowDownRight className="h-4 w-4" />}
                          </div>
                          <div>
                            <p className="text-sm font-medium text-gray-800">
                              {entry.type === 'deposit' ? 'Aporte' : 'Resgate'}
                            </p>
                            <p className="text-xs text-gray-500">{formatDate(entry.date)}</p>
                          </div>
                        </div>
                        <p className={`font-semibold ${entry.type === 'deposit' ? 'text-green-600' : 'text-red-600'}`}>
                          {entry.type === 'deposit' ? '+' : '-'} {formatCurrency(entry.amount)}
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </>
          ) : (
            <div className="flex h-64 flex-col items-center justify-center text-gray-400">
              <TrendingUp className="mb-4 h-12 w-12" />
              <p>Selecione uma carteira para ver detalhes</p>
            </div>
          )}
        </Card>
      </div>

      {/* Modal Nova Carteira */}
      <Modal isOpen={isPortfolioModalOpen} onClose={() => setIsPortfolioModalOpen(false)} title="Nova Carteira" size="md">
        {error && <div className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-600">{error}</div>}
        <form onSubmit={handleCreatePortfolio} className="space-y-4">
          <Input label="Nome" placeholder="Ex: Renda Fixa" value={portfolioForm.name} onChange={(e) => setPortfolioForm({ ...portfolioForm, name: e.target.value })} required />
          <Input label="Tipo" placeholder="Ex: Renda Fixa, Ações, Misto" value={portfolioForm.type} onChange={(e) => setPortfolioForm({ ...portfolioForm, type: e.target.value })} />
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="ghost" onClick={() => setIsPortfolioModalOpen(false)}>Cancelar</Button>
            <Button type="submit" isLoading={formLoading}>Criar Carteira</Button>
          </div>
        </form>
      </Modal>

      {/* Modal Nova Movimentação */}
      <Modal isOpen={isEntryModalOpen} onClose={() => setIsEntryModalOpen(false)} title="Registrar Movimentação" size="md">
        {error && <div className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-600">{error}</div>}
        <form onSubmit={handleCreateEntry} className="space-y-4">
          <div className="flex gap-4">
            <button
              type="button"
              onClick={() => setEntryForm({ ...entryForm, type: 'deposit' })}
              className={`flex-1 rounded-lg border-2 p-4 text-center ${entryForm.type === 'deposit' ? 'border-green-500 bg-green-50' : 'border-gray-200'}`}
            >
              <ArrowUpRight className={`mx-auto h-6 w-6 ${entryForm.type === 'deposit' ? 'text-green-600' : 'text-gray-400'}`} />
              <p className={`mt-1 font-medium ${entryForm.type === 'deposit' ? 'text-green-600' : 'text-gray-500'}`}>Aporte</p>
            </button>
            <button
              type="button"
              onClick={() => setEntryForm({ ...entryForm, type: 'withdrawal' })}
              className={`flex-1 rounded-lg border-2 p-4 text-center ${entryForm.type === 'withdrawal' ? 'border-red-500 bg-red-50' : 'border-gray-200'}`}
            >
              <ArrowDownRight className={`mx-auto h-6 w-6 ${entryForm.type === 'withdrawal' ? 'text-red-600' : 'text-gray-400'}`} />
              <p className={`mt-1 font-medium ${entryForm.type === 'withdrawal' ? 'text-red-600' : 'text-gray-500'}`}>Resgate</p>
            </button>
          </div>
          <Input label="Valor" type="number" step="0.01" min="0.01" value={entryForm.amount || ''} onChange={(e) => setEntryForm({ ...entryForm, amount: parseFloat(e.target.value) || 0 })} required />
          <Input label="Data" type="date" value={entryForm.date} onChange={(e) => setEntryForm({ ...entryForm, date: e.target.value })} required />
          <Input label="Descrição (opcional)" placeholder="Ex: Tesouro Selic" value={entryForm.description} onChange={(e) => setEntryForm({ ...entryForm, description: e.target.value })} />
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="ghost" onClick={() => setIsEntryModalOpen(false)}>Cancelar</Button>
            <Button type="submit" isLoading={formLoading}>Registrar</Button>
          </div>
        </form>
      </Modal>
    </AppLayout>
  );
}
