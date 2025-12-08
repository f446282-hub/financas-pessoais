'use client';

import { useEffect, useState } from 'react';
import { AppLayout } from '@/components/layout';
import { Card, CardHeader, Button, Input, Select, Modal, Badge } from '@/components/ui';
import { accountsApi, getErrorMessage } from '@/services';
import { Account, CreditCard, AccountCreate, CreditCardCreate, AccountType } from '@/types';
import { formatCurrency, formatAccountType } from '@/utils/formatters';
import { Plus, Wallet, CreditCard as CreditCardIcon, Building, Trash2, Edit } from 'lucide-react';

export default function ContasPage() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [cards, setCards] = useState<CreditCard[]>([]);
  const [totalBalance, setTotalBalance] = useState(0);
  const [totalLimit, setTotalLimit] = useState(0);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'accounts' | 'cards'>('accounts');
  
  // Modais
  const [isAccountModalOpen, setIsAccountModalOpen] = useState(false);
  const [isCardModalOpen, setIsCardModalOpen] = useState(false);
  const [formLoading, setFormLoading] = useState(false);
  const [error, setError] = useState('');

  // Forms
  const [accountForm, setAccountForm] = useState<AccountCreate>({
    name: '',
    type: 'checking',
    institution: '',
    initial_balance: 0,
    color: '#166534',
  });

  const [cardForm, setCardForm] = useState<CreditCardCreate>({
    name: '',
    institution: '',
    limit: 0,
    closing_day: 1,
    due_day: 10,
    color: '#166534',
  });

  const fetchData = async () => {
    try {
      setLoading(true);
      const [accRes, cardRes] = await Promise.all([
        accountsApi.getAccounts(),
        accountsApi.getCreditCards(),
      ]);
      setAccounts(accRes.accounts);
      setTotalBalance(accRes.total_balance);
      setCards(cardRes.cards);
      setTotalLimit(cardRes.total_limit);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleCreateAccount = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setFormLoading(true);
    try {
      await accountsApi.createAccount(accountForm);
      setIsAccountModalOpen(false);
      setAccountForm({ name: '', type: 'checking', institution: '', initial_balance: 0, color: '#166534' });
      fetchData();
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setFormLoading(false);
    }
  };

  const handleCreateCard = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setFormLoading(true);
    try {
      await accountsApi.createCreditCard(cardForm);
      setIsCardModalOpen(false);
      setCardForm({ name: '', institution: '', limit: 0, closing_day: 1, due_day: 10, color: '#166534' });
      fetchData();
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setFormLoading(false);
    }
  };

  const handleDeleteAccount = async (id: string) => {
    if (!confirm('Deseja realmente excluir esta conta?')) return;
    try {
      await accountsApi.deleteAccount(id);
      fetchData();
    } catch (err) {
      alert(getErrorMessage(err));
    }
  };

  const handleDeleteCard = async (id: string) => {
    if (!confirm('Deseja realmente excluir este cartão?')) return;
    try {
      await accountsApi.deleteCreditCard(id);
      fetchData();
    } catch (err) {
      alert(getErrorMessage(err));
    }
  };

  const accountTypes: { value: AccountType; label: string }[] = [
    { value: 'checking', label: 'Conta Corrente' },
    { value: 'savings', label: 'Poupança' },
    { value: 'wallet', label: 'Carteira' },
    { value: 'investment', label: 'Investimento' },
    { value: 'other', label: 'Outra' },
  ];

  return (
    <AppLayout title="Contas & Cartões">
      {/* Resumo */}
      <div className="mb-6 grid gap-6 md:grid-cols-2">
        <Card className="bg-gradient-to-br from-primary-700 to-primary-800 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-primary-200">Saldo Total em Contas</p>
              <p className="mt-2 text-3xl font-bold">{formatCurrency(totalBalance)}</p>
              <p className="mt-1 text-sm text-primary-200">{accounts.length} conta(s) ativa(s)</p>
            </div>
            <div className="rounded-xl bg-white/10 p-4">
              <Wallet className="h-8 w-8" />
            </div>
          </div>
        </Card>
        <Card className="bg-gradient-to-br from-purple-600 to-purple-700 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-purple-200">Limite Total em Cartões</p>
              <p className="mt-2 text-3xl font-bold">{formatCurrency(totalLimit)}</p>
              <p className="mt-1 text-sm text-purple-200">{cards.length} cartão(ões) ativo(s)</p>
            </div>
            <div className="rounded-xl bg-white/10 p-4">
              <CreditCardIcon className="h-8 w-8" />
            </div>
          </div>
        </Card>
      </div>

      {/* Tabs */}
      <div className="mb-6 flex items-center justify-between">
        <div className="flex border-b border-gray-200">
          <button
            onClick={() => setActiveTab('accounts')}
            className={`px-6 py-3 text-sm font-medium ${activeTab === 'accounts' ? 'border-b-2 border-primary-700 text-primary-700' : 'text-gray-500 hover:text-gray-700'}`}
          >
            <Wallet className="mr-2 inline h-4 w-4" />
            Contas ({accounts.length})
          </button>
          <button
            onClick={() => setActiveTab('cards')}
            className={`px-6 py-3 text-sm font-medium ${activeTab === 'cards' ? 'border-b-2 border-primary-700 text-primary-700' : 'text-gray-500 hover:text-gray-700'}`}
          >
            <CreditCardIcon className="mr-2 inline h-4 w-4" />
            Cartões ({cards.length})
          </button>
        </div>
        <Button
          leftIcon={<Plus className="h-4 w-4" />}
          onClick={() => activeTab === 'accounts' ? setIsAccountModalOpen(true) : setIsCardModalOpen(true)}
        >
          {activeTab === 'accounts' ? 'Nova Conta' : 'Novo Cartão'}
        </Button>
      </div>

      {/* Conteúdo */}
      {loading ? (
        <div className="flex h-64 items-center justify-center">
          <div className="h-12 w-12 spinner" />
        </div>
      ) : activeTab === 'accounts' ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {accounts.map((account) => (
            <Card key={account.id} className="card-hover">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="rounded-lg p-2" style={{ backgroundColor: account.color || '#166534' }}>
                    <Wallet className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <p className="font-semibold text-gray-800">{account.name}</p>
                    <p className="text-sm text-gray-500">{account.institution || formatAccountType(account.type)}</p>
                  </div>
                </div>
                <button
                  onClick={() => handleDeleteAccount(account.id)}
                  className="rounded p-1 text-gray-400 hover:bg-red-50 hover:text-red-600"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
              <div className="mt-4">
                <p className="text-sm text-gray-500">Saldo atual</p>
                <p className={`text-2xl font-bold ${account.current_balance >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {formatCurrency(account.current_balance)}
                </p>
              </div>
              <div className="mt-3">
                <Badge variant="default" size="sm">{formatAccountType(account.type)}</Badge>
              </div>
            </Card>
          ))}
          {accounts.length === 0 && (
            <div className="col-span-full flex h-48 items-center justify-center text-gray-400">
              Nenhuma conta cadastrada
            </div>
          )}
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {cards.map((card) => (
            <Card key={card.id} className="card-hover overflow-hidden">
              <div
                className="h-32 rounded-lg p-4 text-white"
                style={{ background: `linear-gradient(135deg, ${card.color || '#166534'}, ${card.color || '#166534'}dd)` }}
              >
                <div className="flex h-full flex-col justify-between">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-sm opacity-80">{card.institution}</p>
                      <p className="font-semibold">{card.name}</p>
                    </div>
                    <CreditCardIcon className="h-8 w-8 opacity-50" />
                  </div>
                  <div className="flex items-end justify-between">
                    <div>
                      <p className="text-xs opacity-70">Limite</p>
                      <p className="font-bold">{formatCurrency(card.limit)}</p>
                    </div>
                    <button
                      onClick={() => handleDeleteCard(card.id)}
                      className="rounded p-1 text-white/70 hover:bg-white/20 hover:text-white"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
              <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-gray-500">Fechamento</p>
                  <p className="font-medium text-gray-800">Dia {card.closing_day}</p>
                </div>
                <div>
                  <p className="text-gray-500">Vencimento</p>
                  <p className="font-medium text-gray-800">Dia {card.due_day}</p>
                </div>
              </div>
            </Card>
          ))}
          {cards.length === 0 && (
            <div className="col-span-full flex h-48 items-center justify-center text-gray-400">
              Nenhum cartão cadastrado
            </div>
          )}
        </div>
      )}

      {/* Modal Nova Conta */}
      <Modal isOpen={isAccountModalOpen} onClose={() => setIsAccountModalOpen(false)} title="Nova Conta" size="md">
        {error && <div className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-600">{error}</div>}
        <form onSubmit={handleCreateAccount} className="space-y-4">
          <Input label="Nome" placeholder="Ex: Nubank" value={accountForm.name} onChange={(e) => setAccountForm({ ...accountForm, name: e.target.value })} required />
          <Select label="Tipo" options={accountTypes} value={accountForm.type} onChange={(e) => setAccountForm({ ...accountForm, type: e.target.value as AccountType })} />
          <Input label="Instituição" placeholder="Ex: Nubank" value={accountForm.institution || ''} onChange={(e) => setAccountForm({ ...accountForm, institution: e.target.value })} />
          <Input label="Saldo Inicial" type="number" step="0.01" value={accountForm.initial_balance || ''} onChange={(e) => setAccountForm({ ...accountForm, initial_balance: parseFloat(e.target.value) || 0 })} />
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="ghost" onClick={() => setIsAccountModalOpen(false)}>Cancelar</Button>
            <Button type="submit" isLoading={formLoading}>Criar Conta</Button>
          </div>
        </form>
      </Modal>

      {/* Modal Novo Cartão */}
      <Modal isOpen={isCardModalOpen} onClose={() => setIsCardModalOpen(false)} title="Novo Cartão" size="md">
        {error && <div className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-600">{error}</div>}
        <form onSubmit={handleCreateCard} className="space-y-4">
          <Input label="Nome do Cartão" placeholder="Ex: Nubank Platinum" value={cardForm.name} onChange={(e) => setCardForm({ ...cardForm, name: e.target.value })} required />
          <Input label="Banco Emissor" placeholder="Ex: Nubank" value={cardForm.institution} onChange={(e) => setCardForm({ ...cardForm, institution: e.target.value })} required />
          <Input label="Limite" type="number" step="0.01" value={cardForm.limit || ''} onChange={(e) => setCardForm({ ...cardForm, limit: parseFloat(e.target.value) || 0 })} required />
          <div className="grid grid-cols-2 gap-4">
            <Input label="Dia Fechamento" type="number" min="1" max="31" value={cardForm.closing_day} onChange={(e) => setCardForm({ ...cardForm, closing_day: parseInt(e.target.value) || 1 })} required />
            <Input label="Dia Vencimento" type="number" min="1" max="31" value={cardForm.due_day} onChange={(e) => setCardForm({ ...cardForm, due_day: parseInt(e.target.value) || 10 })} required />
          </div>
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="ghost" onClick={() => setIsCardModalOpen(false)}>Cancelar</Button>
            <Button type="submit" isLoading={formLoading}>Criar Cartão</Button>
          </div>
        </form>
      </Modal>
    </AppLayout>
  );
}
