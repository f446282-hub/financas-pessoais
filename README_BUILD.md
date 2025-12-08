# 🚀 Build de Executáveis - Finanças Pessoais

## ⚡ Início Rápido

Para gerar executáveis para distribuição:

```cmd
build_completo.bat
```

**Tempo estimado:** 5-15 minutos  
**Resultado:** Pasta `distribuicao/` pronta para distribuir

## 📚 Documentação Completa

- **Para Product Managers**: Veja [`GUIA_PRODUCT_MANAGER.md`](GUIA_PRODUCT_MANAGER.md)
- **Para Desenvolvedores**: Veja [`GUIA_BUILD.md`](GUIA_BUILD.md)

## 🎯 O Que Este Build Gera

1. ✅ **Backend Executável** (`financas-backend.exe`)
   - API FastAPI completa
   - Inclui todas as dependências
   - Pronto para rodar

2. ✅ **Frontend Buildado**
   - Interface web otimizada
   - Pronta para produção

3. ✅ **Launcher Automático**
   - Inicia backend + frontend
   - Abre navegador automaticamente

4. ✅ **Documentação**
   - Instruções para o cliente final

## 🔧 Pré-requisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (para desenvolvimento)
- Microsoft Visual C++ Build Tools (para psycopg2)

## 📦 Estrutura Após Build

```
distribuicao/
├── financas-backend.exe
├── .env.example
├── Iniciar_Financas_Pessoais.bat
├── LEIA-ME.txt
└── frontend/
```

## 🎁 Distribuição

1. Compacte a pasta `distribuicao/` em ZIP
2. Envie para o cliente
3. Cliente extrai e executa `Iniciar_Financas_Pessoais.bat`

## 🆘 Ajuda

- Problemas de build? Veja [`GUIA_BUILD.md`](GUIA_BUILD.md)
- Dúvidas de distribuição? Veja [`GUIA_PRODUCT_MANAGER.md`](GUIA_PRODUCT_MANAGER.md)

---

**Desenvolvido para facilitar a distribuição do sistema Finanças Pessoais**

