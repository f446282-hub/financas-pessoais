# 💰 Finanças Pessoais - Frontend

Interface web para o sistema de gestão financeira pessoal.

## 🚀 Quick Start

### Windows (Recomendado)

1. **Instalação completa:**
   ```cmd
   setup_windows.bat
   ```

2. **Iniciar servidor:**
   ```cmd
   run_windows.bat
   ```

### Linux/Mac

```bash
# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env.local

# Iniciar servidor de desenvolvimento
npm run dev
```

Acesse: http://localhost:3000

## 🏗️ Estrutura

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx          # Layout raiz
│   │   ├── page.tsx            # Dashboard (/)
│   │   ├── login/              # Autenticação
│   │   ├── lancamentos/        # Transações
│   │   ├── contas/             # Contas & Cartões
│   │   ├── investimentos/      # Investimentos
│   │   ├── indicadores/        # Indicadores
│   │   ├── integracoes/        # Integrações
│   │   └── configuracoes/      # Configurações
│   ├── components/
│   │   ├── ui/                 # Componentes base (Button, Card, Input...)
│   │   ├── layout/             # Layout components (Sidebar, Topbar...)
│   │   └── charts/             # Gráficos dinâmicos
│   ├── services/               # API Services
│   ├── hooks/                  # Custom hooks
│   ├── types/                  # TypeScript types
│   └── utils/                  # Utilitários
├── public/
└── package.json
```

## 📊 Gráficos Implementados

1. **CashFlowLineChart** - Fluxo de caixa diário (Receitas vs Despesas)
2. **MonthlyComparisonBarChart** - Comparação mensal em barras
3. **ExpensesPieChart** - Distribuição de despesas por categoria (Pizza/Donut)
4. **InvestmentAreaChart** - Evolução de investimentos (Área)
5. **DonutChart** - Gráfico de rosca genérico

## 🎨 Design System

### Cores

- **Primary**: Verde escuro (#166534)
- **Success**: Verde (#22c55e)
- **Warning**: Amarelo (#f59e0b)
- **Error**: Vermelho (#ef4444)
- **Info**: Azul (#3b82f6)

### Componentes

- `Button` - Botões com variantes (primary, secondary, outline, ghost, danger)
- `Card` - Cards com header opcional
- `Input` - Inputs com label e validação
- `Select` - Selects estilizados
- `Badge` - Badges de status
- `Modal` - Modais responsivos

## 🔧 Variáveis de Ambiente

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=Finanças Pessoais
```

## 📱 Páginas

| Rota | Descrição |
|------|-----------|
| `/` | Dashboard com gráficos e resumo |
| `/login` | Autenticação |
| `/lancamentos` | Lista e cadastro de transações |
| `/contas` | Gestão de contas e cartões |
| `/investimentos` | Carteiras de investimento |
| `/indicadores` | Métricas financeiras |
| `/integracoes` | Bancos e WhatsApp |
| `/configuracoes` | Perfil e preferências |

## 🛠️ Stack

- **Next.js 14** - Framework React
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Estilização
- **Recharts** - Gráficos
- **Axios** - HTTP Client
- **Lucide React** - Ícones
- **date-fns** - Manipulação de datas

## 📄 Licença

Projeto privado - Todos os direitos reservados.
