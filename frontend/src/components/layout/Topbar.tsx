'use client';

import { useEffect, useState } from 'react';
import { Bell, User } from 'lucide-react';
import { authApi } from '@/services';
import { User as UserType } from '@/types';

interface TopbarProps {
  title?: string;
}

export default function Topbar({ title }: TopbarProps) {
  const [user, setUser] = useState<UserType | null>(null);

  useEffect(() => {
    const storedUser = authApi.getUser();
    setUser(storedUser);
  }, []);

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-gray-200 bg-white px-6">
      {/* Título da página */}
      <div>
        <h2 className="text-xl font-semibold text-gray-800">{title || 'Dashboard'}</h2>
      </div>

      {/* Ações */}
      <div className="flex items-center gap-4">
        {/* Notificações */}
        <button className="relative rounded-full p-2 text-gray-500 hover:bg-gray-100 hover:text-gray-700">
          <Bell size={20} />
          <span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-red-500" />
        </button>

        {/* Perfil */}
        <div className="flex items-center gap-3">
          <div className="text-right">
            <p className="text-sm font-medium text-gray-800">{user?.name || 'Usuário'}</p>
            <p className="text-xs text-gray-500">{user?.email || ''}</p>
          </div>
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary-100 text-primary-700">
            <User size={20} />
          </div>
        </div>
      </div>
    </header>
  );
}
