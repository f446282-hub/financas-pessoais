'use client';

import { useEffect, useState } from 'react';
import { AppLayout } from '@/components/layout';
import { Card, CardHeader, Button, Input, Select, Badge, Modal } from '@/components/ui';
import { transactionsApi, accountsApi, getErrorMessage } from '@/services';
import { Transaction, Category, Account, CreditCard, TransactionCreate } from '@/types';
import { formatCurrency, formatDate, formatTransactionType, getCurrentDate } from '@/utils/formatters';
import { Plus, Search, Filter, Trash2, Edit } from 'lucide-react';

export default function LancamentosPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [cards, setCards] = useState<CreditCard[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formLoading, setFormLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Filtros
  const [filters, setFilters] = useState({
    type: '',
    account_id: '',
    start_date: '',
    end_date: '',
  });

  // Form
  const [form, setForm] = useState<TransactionCreate>({
    type: 'expense',
    description: '',
    amount: 0,
    date: getCurrentDate(),
    account_id: '',
    category_id: '',
    status: 'paid',
    is_recurring: false,
  });

  const fetchData = async () => {
    try {
      setLoading(true);
      const [txRes, catRes, accRes, cardRes] = await Promise.all([
        transactionsApi.getTransactions(filters.type || filters.account_id ? filters as any : undefined),
        transactionsApi.getCategories(),
        accountsApi.getAccounts(),
        accountsApi.getCreditCards(),
      ]);
      setTransactions(txRes.transactions);
      setCategories(catRes);
      setAccounts(accRes.accounts);
      setCards(cardRes.cards);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setFormLoading(true);

    try {
      await transactionsApi.createTransaction({
        ...form,
        account_id: form.account_id || undefined,
        category_id: form.category_id || undefined,
      });
      setIsModalOpen(false);
      setForm({
        type: 'expense',
        description: '',
        amount: 0,
        date: getCurrentDate(),
        account_id: '',
        category_id: '',
        status: 'paid',
        is_recurring: false,
      });
      fetchData();
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setFormLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Deseja realmente excluir este lançamento?')) return;
    try {
      await transactionsApi.deleteTransaction(id);
      fetchData();
    } catch (err) {
      alert(getErrorMessage(err));
    }
  };

  const filteredCategories = categories.filter(c => c.type === form.type);

  return (
    <AppLayout title="Lançamentos">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Buscar lançamentos..."
              className="rounded-lg border border-gray-300 bg-white py-2 pl-10 pr-4 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            />
          </div>
          <select
            className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm"
            value={filters.type}
            onChange={(e) => setFilters({ ...filters, type: e.target.value })}
          >
            <option value="">Todos os tipos</option>
            <option value="income">Receitas</option>
            <option value="expense">Despesas</option>
          </select>
        </div>
        <Button leftIcon={<Plus className="h-4 w-4" />} onClick={() => setIsModalOpen(true)}>
          Novo Lançamento
        </Button>
      </div>

      {/* Tabela */}
      <Card padding="none">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="border-b border-gray-200 bg-gray-50">
              <tr>
                <th className="px-6 py-4 text-left text-xs font-semibold uppercase text-gray-500">Data</th>
                <th className="px-6 py-4 text-left text-xs font-semibold uppercase text-gray-500">Descrição</th>
                <th className="px-6 py-4 text-left text-xs font-semibold uppercase text-gray-500">Categoria</th>
                <th className="px-6 py-4 text-left text-xs font-semibold uppercase text-gray-500">Conta</th>
                <th className="px-6 py-4 text-left text-xs font-semibold uppercase text-gray-500">Tipo</th>
                <th className="px-6 py-4 text-right text-xs font-semibold uppercase text-gray-500">Valor</th>
                <th className="px-6 py-4 text-center text-xs font-semibold uppercase text-gray-500">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {loading ? (
                <tr>
                  <td colSpan={7} className="px-6 py-12 text-center">
                    <div className="mx-auto h-8 w-8 spinner" />
                  </td>
                </tr>
              ) : transactions.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-6 py-12 text-center text-gray-400">
                    Nenhum lançamento encontrado
                  </td>
                </tr>
              ) : (
                transactions.map((tx) => (
                  <tr key={tx.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm text-gray-600">{formatDate(tx.date)}</td>
                    <td className="px-6 py-4">
                      <p className="text-sm font-medium text-gray-800">{tx.description}</p>
                    </td>
                    <td className="px-6 py-4">
                      {tx.category_name && (
                        <div className="flex items-center gap-2">
                          <div
                            className="h-2 w-2 rounded-full"
                            style={{ backgroundColor: tx.category_color || '#6b7280' }}
                          />
                          <span className="text-sm text-gray-600">{tx.category_name}</span>
                        </div>
                      )}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {tx.account_name || tx.credit_card_name || '-'}
                    </td>
                    <td className="px-6 py-4">
                      <Badge variant={tx.type === 'income' ? 'success' : 'error'} size="sm">
                        {formatTransactionType(tx.type)}
                      </Badge>
                    </td>
                    <td className={`px-6 py-4 text-right text-sm font-medium ${tx.type === 'income' ? 'text-green-600' : 'text-red-600'}`}>
                      {tx.type === 'income' ? '+' : '-'} {formatCurrency(tx.amount)}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex justify-center gap-2">
                        <button className="rounded p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600">
                          <Edit className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(tx.id)}
                          className="rounded p-1 text-gray-400 hover:bg-red-50 hover:text-red-600"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Modal de Novo Lançamento */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Novo Lançamento" size="lg">
        {error && (
          <div className="mb-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
            {error}
          </div>
        )}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Select
              label="Tipo"
              options={[
                { value: 'expense', label: 'Despesa' },
                { value: 'income', label: 'Receita' },
              ]}
              value={form.type}
              onChange={(e) => setForm({ ...form, type: e.target.value as any, category_id: '' })}
            />
            <Input
              label="Data"
              type="date"
              value={form.date}
              onChange={(e) => setForm({ ...form, date: e.target.value })}
              required
            />
          </div>

          <Input
            label="Descrição"
            placeholder="Ex: Almoço no restaurante"
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            required
          />

          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Valor"
              type="number"
              step="0.01"
              min="0.01"
              placeholder="0,00"
              value={form.amount || ''}
              onChange={(e) => setForm({ ...form, amount: parseFloat(e.target.value) || 0 })}
              required
            />
            <Select
              label="Conta"
              options={accounts.map((a) => ({ value: a.id, label: a.name }))}
              value={form.account_id || ''}
              onChange={(e) => setForm({ ...form, account_id: e.target.value })}
              placeholder="Selecione uma conta"
            />
          </div>

          <Select
            label="Categoria"
            options={filteredCategories.map((c) => ({ value: c.id, label: c.name }))}
            value={form.category_id || ''}
            onChange={(e) => setForm({ ...form, category_id: e.target.value })}
            placeholder="Selecione uma categoria"
          />

          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="ghost" onClick={() => setIsModalOpen(false)}>
              Cancelar
            </Button>
            <Button type="submit" isLoading={formLoading}>
              Salvar Lançamento
            </Button>
          </div>
        </form>
      </Modal>
    </AppLayout>
  );
}
