'use client';

import { useEffect, useState } from 'react';
import { AppLayout } from '@/components/layout';
import { Card, CardHeader, Button, Input } from '@/components/ui';
import { authApi, getErrorMessage } from '@/services';
import { User } from '@/types';
import { User as UserIcon, Mail, Lock, Save, Shield } from 'lucide-react';

export default function ConfiguracoesPage() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  const [profileForm, setProfileForm] = useState({ name: '' });
  const [passwordForm, setPasswordForm] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  useEffect(() => {
    const storedUser = authApi.getUser();
    if (storedUser) {
      setUser(storedUser);
      setProfileForm({ name: storedUser.name });
    }
    setLoading(false);
  }, []);

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage({ type: '', text: '' });

    try {
      const updatedUser = await authApi.updateProfile({ name: profileForm.name });
      setUser(updatedUser);
      authApi.saveAuth(authApi.getToken()!, updatedUser);
      setMessage({ type: 'success', text: 'Perfil atualizado com sucesso!' });
    } catch (err) {
      setMessage({ type: 'error', text: getErrorMessage(err) });
    } finally {
      setSaving(false);
    }
  };

  const handleUpdatePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      setMessage({ type: 'error', text: 'As senhas não coincidem' });
      return;
    }

    if (passwordForm.newPassword.length < 6) {
      setMessage({ type: 'error', text: 'A nova senha deve ter no mínimo 6 caracteres' });
      return;
    }

    setSaving(true);
    setMessage({ type: '', text: '' });

    try {
      await authApi.updatePassword(passwordForm.currentPassword, passwordForm.newPassword);
      setPasswordForm({ currentPassword: '', newPassword: '', confirmPassword: '' });
      setMessage({ type: 'success', text: 'Senha alterada com sucesso!' });
    } catch (err) {
      setMessage({ type: 'error', text: getErrorMessage(err) });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <AppLayout title="Configurações">
        <div className="flex h-64 items-center justify-center">
          <div className="h-12 w-12 spinner" />
        </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout title="Configurações">
      {message.text && (
        <div
          className={`mb-6 rounded-lg border p-4 ${
            message.type === 'success'
              ? 'border-green-200 bg-green-50 text-green-700'
              : 'border-red-200 bg-red-50 text-red-700'
          }`}
        >
          {message.text}
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Perfil */}
        <Card>
          <CardHeader
            title="Perfil"
            subtitle="Atualize suas informações pessoais"
          />
          <form onSubmit={handleUpdateProfile} className="space-y-4">
            <div className="flex items-center gap-4">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary-100 text-primary-700">
                <UserIcon className="h-8 w-8" />
              </div>
              <div>
                <p className="font-semibold text-gray-800">{user?.name}</p>
                <p className="text-sm text-gray-500">{user?.email}</p>
              </div>
            </div>

            <Input
              label="Nome"
              value={profileForm.name}
              onChange={(e) => setProfileForm({ ...profileForm, name: e.target.value })}
              required
            />

            <Input
              label="Email"
              value={user?.email || ''}
              disabled
              helperText="O email não pode ser alterado"
            />

            <Button type="submit" leftIcon={<Save className="h-4 w-4" />} isLoading={saving}>
              Salvar Alterações
            </Button>
          </form>
        </Card>

        {/* Segurança */}
        <Card>
          <CardHeader
            title="Segurança"
            subtitle="Altere sua senha de acesso"
          />
          <form onSubmit={handleUpdatePassword} className="space-y-4">
            <div className="flex items-center gap-3 rounded-lg bg-yellow-50 p-4">
              <Shield className="h-5 w-5 text-yellow-600" />
              <p className="text-sm text-yellow-700">
                Use uma senha forte com letras, números e caracteres especiais
              </p>
            </div>

            <Input
              label="Senha Atual"
              type="password"
              value={passwordForm.currentPassword}
              onChange={(e) => setPasswordForm({ ...passwordForm, currentPassword: e.target.value })}
              required
            />

            <Input
              label="Nova Senha"
              type="password"
              value={passwordForm.newPassword}
              onChange={(e) => setPasswordForm({ ...passwordForm, newPassword: e.target.value })}
              required
            />

            <Input
              label="Confirmar Nova Senha"
              type="password"
              value={passwordForm.confirmPassword}
              onChange={(e) => setPasswordForm({ ...passwordForm, confirmPassword: e.target.value })}
              required
            />

            <Button type="submit" leftIcon={<Lock className="h-4 w-4" />} isLoading={saving}>
              Alterar Senha
            </Button>
          </form>
        </Card>

        {/* Preferências */}
        <Card className="lg:col-span-2">
          <CardHeader
            title="Preferências"
            subtitle="Personalize sua experiência"
          />
          <div className="grid gap-6 md:grid-cols-2">
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">Moeda</label>
              <select className="w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm" disabled>
                <option>Real Brasileiro (R$)</option>
              </select>
              <p className="mt-1 text-xs text-gray-500">Mais moedas em breve</p>
            </div>

            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">Fuso Horário</label>
              <select className="w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm" disabled>
                <option>Brasília (GMT-3)</option>
              </select>
              <p className="mt-1 text-xs text-gray-500">Mais fusos em breve</p>
            </div>
          </div>
        </Card>
      </div>
    </AppLayout>
  );
}
