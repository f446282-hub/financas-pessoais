'use client';

import { TrendingUp } from 'lucide-react';

interface AuthLayoutProps {
  children: React.ReactNode;
}

export default function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div className="flex min-h-screen">
      {/* Lado esquerdo - Formulário */}
      <div className="flex w-full flex-col justify-center px-8 lg:w-1/2 lg:px-16">
        <div className="mx-auto w-full max-w-md">
          {/* Logo */}
          <div className="mb-8 flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-700 text-white">
              <TrendingUp className="h-7 w-7" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-800">Finanças</h1>
              <p className="text-sm text-gray-500">Pessoais</p>
            </div>
          </div>

          {children}
        </div>
      </div>

      {/* Lado direito - Visual */}
      <div className="hidden bg-gradient-to-br from-primary-700 to-primary-900 lg:flex lg:w-1/2 lg:flex-col lg:items-center lg:justify-center lg:p-16">
        <div className="text-center text-white">
          <h2 className="mb-4 text-4xl font-bold">Controle suas finanças</h2>
          <p className="mb-8 text-lg text-primary-200">
            Tenha uma visão completa do seu dinheiro com dashboards inteligentes, gráficos dinâmicos
            e indicadores personalizados.
          </p>
          <div className="grid grid-cols-2 gap-6 text-left">
            <div className="rounded-xl bg-white/10 p-4">
              <div className="mb-2 text-2xl font-bold">📊</div>
              <h3 className="font-semibold">Dashboard completo</h3>
              <p className="text-sm text-primary-200">Visualize tudo em tempo real</p>
            </div>
            <div className="rounded-xl bg-white/10 p-4">
              <div className="mb-2 text-2xl font-bold">💳</div>
              <h3 className="font-semibold">Contas & Cartões</h3>
              <p className="text-sm text-primary-200">Gerencie todas suas contas</p>
            </div>
            <div className="rounded-xl bg-white/10 p-4">
              <div className="mb-2 text-2xl font-bold">📈</div>
              <h3 className="font-semibold">Investimentos</h3>
              <p className="text-sm text-primary-200">Acompanhe seu patrimônio</p>
            </div>
            <div className="rounded-xl bg-white/10 p-4">
              <div className="mb-2 text-2xl font-bold">🎯</div>
              <h3 className="font-semibold">Metas</h3>
              <p className="text-sm text-primary-200">Alcance seus objetivos</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
