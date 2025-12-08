'use client';

import { useEffect, useState } from 'react';
import { AppLayout } from '@/components/layout';
import { Card, CardHeader, Button, Input, Badge } from '@/components/ui';
import { integrationsApi, getErrorMessage } from '@/services';
import { BankProvider, BankIntegration, WhatsAppSettings } from '@/types';
import { formatDateTime } from '@/utils/formatters';
import { Building, MessageCircle, Check, X, RefreshCw, Phone, Bell, Calendar } from 'lucide-react';

export default function IntegracoesPage() {
  const [bankProviders, setBankProviders] = useState<BankProvider[]>([]);
  const [bankIntegrations, setBankIntegrations] = useState<BankIntegration[]>([]);
  const [whatsappSettings, setWhatsappSettings] = useState<WhatsAppSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const [phoneNumber, setPhoneNumber] = useState('');

  const fetchData = async () => {
    try {
      setLoading(true);
      const [providers, integrations, whatsapp] = await Promise.all([
        integrationsApi.getBankProviders(),
        integrationsApi.getBankIntegrations(),
        integrationsApi.getWhatsAppSettings(),
      ]);
      setBankProviders(providers);
      setBankIntegrations(integrations);
      setWhatsappSettings(whatsapp);
      setPhoneNumber(whatsapp.phone_number || '');
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const getIntegrationStatus = (provider: string) => {
    return bankIntegrations.find((i) => i.provider === provider);
  };

  const handleConnect = async (provider: string) => {
    setActionLoading(provider);
    try {
      await integrationsApi.connectBank(provider);
      fetchData();
    } catch (err) {
      alert(getErrorMessage(err));
    } finally {
      setActionLoading(null);
    }
  };

  const handleDisconnect = async (provider: string) => {
    if (!confirm('Deseja desconectar esta integração?')) return;
    setActionLoading(provider);
    try {
      await integrationsApi.disconnectBank(provider);
      fetchData();
    } catch (err) {
      alert(getErrorMessage(err));
    } finally {
      setActionLoading(null);
    }
  };

  const handleSync = async (provider: string) => {
    setActionLoading(`sync-${provider}`);
    try {
      await integrationsApi.syncBank(provider);
      fetchData();
    } catch (err) {
      alert(getErrorMessage(err));
    } finally {
      setActionLoading(null);
    }
  };

  const handleUpdateWhatsapp = async (updates: Partial<WhatsAppSettings>) => {
    try {
      const result = await integrationsApi.updateWhatsAppSettings(updates);
      setWhatsappSettings(result);
    } catch (err) {
      alert(getErrorMessage(err));
    }
  };

  return (
    <AppLayout title="Integrações">
      {loading ? (
        <div className="flex h-64 items-center justify-center">
          <div className="h-12 w-12 spinner" />
        </div>
      ) : (
        <div className="space-y-8">
          {/* Integrações Bancárias */}
          <div>
            <div className="mb-4 flex items-center gap-3">
              <div className="rounded-lg bg-primary-100 p-2">
                <Building className="h-5 w-5 text-primary-700" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-gray-800">Integrações Bancárias</h2>
                <p className="text-sm text-gray-500">Conecte suas contas para importar transações automaticamente</p>
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {bankProviders.map((provider) => {
                const integration = getIntegrationStatus(provider.code);
                const isConnected = integration?.status === 'connected';
                const isLoading = actionLoading === provider.code || actionLoading === `sync-${provider.code}`;

                return (
                  <Card key={provider.code} className="card-hover">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gray-100 text-xl font-bold text-gray-600">
                          {provider.name.charAt(0)}
                        </div>
                        <div>
                          <p className="font-semibold text-gray-800">{provider.name}</p>
                          {isConnected && integration?.last_sync_at && (
                            <p className="text-xs text-gray-500">
                              Sincronizado: {formatDateTime(integration.last_sync_at)}
                            </p>
                          )}
                        </div>
                      </div>
                      <Badge variant={isConnected ? 'success' : 'default'} size="sm">
                        {isConnected ? 'Conectado' : 'Desconectado'}
                      </Badge>
                    </div>

                    <div className="mt-4 flex gap-2">
                      {isConnected ? (
                        <>
                          <Button
                            size="sm"
                            variant="outline"
                            leftIcon={<RefreshCw className={`h-4 w-4 ${actionLoading === `sync-${provider.code}` ? 'animate-spin' : ''}`} />}
                            onClick={() => handleSync(provider.code)}
                            isLoading={actionLoading === `sync-${provider.code}`}
                          >
                            Sincronizar
                          </Button>
                          <Button
                            size="sm"
                            variant="ghost"
                            leftIcon={<X className="h-4 w-4" />}
                            onClick={() => handleDisconnect(provider.code)}
                            isLoading={isLoading && actionLoading === provider.code}
                          >
                            Desconectar
                          </Button>
                        </>
                      ) : (
                        <Button
                          size="sm"
                          leftIcon={<Check className="h-4 w-4" />}
                          onClick={() => handleConnect(provider.code)}
                          isLoading={isLoading}
                        >
                          Conectar
                        </Button>
                      )}
                    </div>
                  </Card>
                );
              })}
            </div>
          </div>

          {/* WhatsApp */}
          <div>
            <div className="mb-4 flex items-center gap-3">
              <div className="rounded-lg bg-green-100 p-2">
                <MessageCircle className="h-5 w-5 text-green-700" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-gray-800">WhatsApp</h2>
                <p className="text-sm text-gray-500">Receba alertas e resumos financeiros no seu WhatsApp</p>
              </div>
            </div>

            <Card>
              <div className="grid gap-6 md:grid-cols-2">
                {/* Número de telefone */}
                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-700">
                    <Phone className="mr-2 inline h-4 w-4" />
                    Número do WhatsApp
                  </label>
                  <div className="flex gap-2">
                    <Input
                      placeholder="+55 11 99999-9999"
                      value={phoneNumber}
                      onChange={(e) => setPhoneNumber(e.target.value)}
                    />
                    <Button
                      onClick={() => handleUpdateWhatsapp({ phone_number: phoneNumber })}
                    >
                      Salvar
                    </Button>
                  </div>
                </div>

                {/* Status */}
                <div className="flex items-center gap-4">
                  <div>
                    <p className="text-sm font-medium text-gray-700">Status</p>
                    <Badge variant={whatsappSettings?.is_active ? 'success' : 'default'}>
                      {whatsappSettings?.is_active ? 'Ativo' : 'Inativo'}
                    </Badge>
                  </div>
                  <Button
                    variant={whatsappSettings?.is_active ? 'outline' : 'primary'}
                    onClick={() => handleUpdateWhatsapp({ is_active: !whatsappSettings?.is_active })}
                  >
                    {whatsappSettings?.is_active ? 'Desativar' : 'Ativar'}
                  </Button>
                </div>
              </div>

              {/* Configurações de alertas */}
              <div className="mt-6 border-t border-gray-200 pt-6">
                <h3 className="mb-4 text-sm font-semibold text-gray-800">Configurações de Alertas</h3>
                <div className="space-y-4">
                  <label className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <Bell className="h-5 w-5 text-gray-400" />
                      <div>
                        <p className="font-medium text-gray-800">Alerta de gastos altos</p>
                        <p className="text-sm text-gray-500">Notificar quando uma despesa for acima do limite</p>
                      </div>
                    </div>
                    <input
                      type="checkbox"
                      checked={whatsappSettings?.alert_on_high_expense || false}
                      onChange={(e) => handleUpdateWhatsapp({ alert_on_high_expense: e.target.checked })}
                      className="h-5 w-5 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                    />
                  </label>

                  <label className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <Calendar className="h-5 w-5 text-gray-400" />
                      <div>
                        <p className="font-medium text-gray-800">Resumo diário</p>
                        <p className="text-sm text-gray-500">Receber resumo das finanças todos os dias</p>
                      </div>
                    </div>
                    <input
                      type="checkbox"
                      checked={whatsappSettings?.daily_summary || false}
                      onChange={(e) => handleUpdateWhatsapp({ daily_summary: e.target.checked })}
                      className="h-5 w-5 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                    />
                  </label>

                  <label className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <Calendar className="h-5 w-5 text-gray-400" />
                      <div>
                        <p className="font-medium text-gray-800">Resumo semanal</p>
                        <p className="text-sm text-gray-500">Receber resumo das finanças toda semana</p>
                      </div>
                    </div>
                    <input
                      type="checkbox"
                      checked={whatsappSettings?.weekly_summary || false}
                      onChange={(e) => handleUpdateWhatsapp({ weekly_summary: e.target.checked })}
                      className="h-5 w-5 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                    />
                  </label>
                </div>
              </div>
            </Card>
          </div>
        </div>
      )}
    </AppLayout>
  );
}
