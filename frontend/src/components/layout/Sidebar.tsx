'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Receipt,
  Wallet,
  PiggyBank,
  Target,
  Link2,
  Settings,
  LogOut,
  TrendingUp,
} from 'lucide-react';
import { authApi } from '@/services';

interface NavItem {
  href: string;
  label: string;
  icon: React.ReactNode;
}

const navItems: NavItem[] = [
  { href: '/', label: 'Dashboard', icon: <LayoutDashboard size={20} /> },
  { href: '/lancamentos', label: 'Lançamentos', icon: <Receipt size={20} /> },
  { href: '/contas', label: 'Contas & Cartões', icon: <Wallet size={20} /> },
  { href: '/investimentos', label: 'Investimentos', icon: <PiggyBank size={20} /> },
  { href: '/indicadores', label: 'Indicadores', icon: <Target size={20} /> },
  { href: '/integracoes', label: 'Integrações', icon: <Link2 size={20} /> },
  { href: '/configuracoes', label: 'Configurações', icon: <Settings size={20} /> },
];

export default function Sidebar() {
  const pathname = usePathname();

  const handleLogout = () => {
    authApi.logout();
    window.location.href = '/login';
  };

  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 bg-primary-700 text-white">
      {/* Logo */}
      <div className="flex h-16 items-center gap-3 border-b border-primary-600 px-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/10">
          <TrendingUp className="h-6 w-6" />
        </div>
        <div>
          <h1 className="text-lg font-bold">Finanças</h1>
          <p className="text-xs text-primary-200">Pessoais</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex flex-col gap-1 p-4">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-all ${
                isActive
                  ? 'bg-white/20 text-white'
                  : 'text-primary-100 hover:bg-white/10 hover:text-white'
              }`}
            >
              {item.icon}
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* Logout */}
      <div className="absolute bottom-0 left-0 right-0 border-t border-primary-600 p-4">
        <button
          onClick={handleLogout}
          className="flex w-full items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium text-primary-100 transition-all hover:bg-white/10 hover:text-white"
        >
          <LogOut size={20} />
          Sair
        </button>
      </div>
    </aside>
  );
}
