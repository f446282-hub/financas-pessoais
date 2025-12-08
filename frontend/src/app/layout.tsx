import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Finanças Pessoais',
  description: 'Plataforma completa de gestão financeira pessoal',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
