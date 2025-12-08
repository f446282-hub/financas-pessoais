# 🚀 Guia de Build e Distribuição - Finanças Pessoais

Este guia explica como gerar executáveis para distribuição do sistema Finanças Pessoais.

## 📋 Visão Geral

O sistema é composto por:
- **Backend**: API FastAPI (Python) → Executável `.exe`
- **Frontend**: Interface Next.js (React) → Build estático

## 🔧 Pré-requisitos

### Para Build

1. **Python 3.11+** instalado
2. **Node.js 18+** e npm instalados
3. **PostgreSQL 15+** (para o ambiente de desenvolvimento)
4. **Microsoft Visual C++ Build Tools** (para compilar dependências Python)

### Para Distribuição

- Windows 10/11 64-bit
- PostgreSQL instalado no sistema do cliente
- Conexão com internet (para configuração inicial)

## 🛠️ Métodos de Build

### Método 1: Build Completo Automatizado (Recomendado)

Execute o script que faz tudo automaticamente:

```cmd
build_completo.bat
```

Este script:
1. ✅ Builda o backend em executável
2. ✅ Builda o frontend para produção
3. ✅ Cria pacote de distribuição completo
4. ✅ Gera launcher e documentação

**Resultado:** Pasta `distribuicao/` com tudo pronto para distribuir.

### Método 2: Build Manual Passo a Passo

#### 2.1. Build do Backend

```cmd
cd backend
venv\Scripts\activate.bat
python -m pip install -r requirements-build.txt
python build_executable.py
```

Ou use o script automatizado:

```cmd
cd backend
build_windows.bat
```

**Resultado:** `backend/dist/financas-backend.exe`

#### 2.2. Build do Frontend

```cmd
cd frontend
npm install
npm run build
```

**Resultado:** Pasta `frontend/.next/` ou `frontend/out/` (dependendo da configuração)

## 📦 Estrutura do Pacote de Distribuição

Após o build completo, você terá:

```
distribuicao/
├── financas-backend.exe          # Executável do backend
├── .env.example                  # Exemplo de configuração
├── Iniciar_Financas_Pessoais.bat # Launcher principal
├── LEIA-ME.txt                   # Documentação para o usuário
└── frontend/                     # Build do frontend
    ├── .next/
    ├── public/
    └── ...
```

## 🎯 Como Distribuir

### Opção 1: Distribuição Simples

1. Compacte a pasta `distribuicao/` em um ZIP
2. Envie para o cliente
3. Instruções:
   - Extrair o ZIP
   - Configurar `.env` com credenciais do PostgreSQL
   - Executar `Iniciar_Financas_Pessoais.bat`

### Opção 2: Instalador (Recomendado para PM)

Para uma experiência profissional, crie um instalador usando:

- **Inno Setup** (gratuito): https://jrsoftware.org/isinfo.php
- **NSIS** (gratuito): https://nsis.sourceforge.io/
- **WiX Toolset** (gratuito): https://wixtoolset.org/

O instalador deve:
1. Criar pasta de instalação
2. Copiar arquivos
3. Configurar atalho no menu Iniciar
4. Opcional: Instalar PostgreSQL automaticamente

## ⚙️ Configuração para o Cliente

O cliente precisa configurar:

### 1. Arquivo `.env`

Copie `.env.example` para `.env` e configure:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/financas_pessoais
SECRET_KEY=sua-chave-secreta-aqui
```

### 2. Banco de Dados

O cliente precisa:
1. Ter PostgreSQL instalado
2. Criar o banco `financas_pessoais`
3. Executar migrations (pode ser automatizado no launcher)

## 🚀 Launcher Automatizado

O arquivo `Iniciar_Financas_Pessoais.bat` faz:

1. ✅ Inicia o backend em janela separada
2. ✅ Aguarda o backend estar pronto
3. ✅ Abre o navegador automaticamente
4. ✅ Permite encerrar o backend facilmente

## 🔍 Troubleshooting

### Erro ao buildar backend

- **Problema**: PyInstaller não encontra módulos
- **Solução**: Adicione `--hidden-import` no `build_executable.py`

### Erro ao buildar frontend

- **Problema**: Erros de dependências
- **Solução**: Execute `npm install` novamente

### Executável não inicia

- **Problema**: Erro de DLL ou dependências
- **Solução**: Use `--onefile` no PyInstaller (já está configurado)

### Frontend não conecta no backend

- **Problema**: CORS ou URL incorreta
- **Solução**: Configure `NEXT_PUBLIC_API_URL` no `.env` do frontend

## 📝 Notas para Product Manager

### Tamanho do Executável

- Backend: ~50-100 MB (inclui Python e todas as dependências)
- Frontend: ~10-20 MB (build otimizado)
- **Total:** ~70-120 MB

### Dependências Externas

O cliente precisa ter:
- ✅ PostgreSQL instalado
- ✅ Navegador moderno (Chrome, Firefox, Edge)

### Atualizações

Para atualizar:
1. Rebuild do executável
2. Substituir arquivos na pasta de instalação
3. Ou criar sistema de auto-update (requer desenvolvimento adicional)

## 🎁 Próximos Passos Recomendados

1. **Instalador Profissional**: Criar instalador com Inno Setup
2. **Auto-Update**: Sistema de atualização automática
3. **Portable**: Versão que não precisa instalar PostgreSQL
4. **Docker**: Container com tudo incluído (mais avançado)

## 📞 Suporte

Para dúvidas sobre build ou distribuição, consulte:
- Documentação do PyInstaller: https://pyinstaller.org/
- Documentação do Next.js: https://nextjs.org/docs

---

**Última atualização:** 2024

