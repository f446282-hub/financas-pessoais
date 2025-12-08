# ⚡ Início Rápido - Resolva o Erro do Rust AGORA

## 🚨 Você está vendo erro do Rust?

```
Cargo, the Rust package manager, is not installed
ERRO: Falha ao instalar dependencias!
```

## ✅ SOLUÇÃO RÁPIDA (1 Comando)

Execute este script:

```cmd
instalar_tudo_windows.bat
```

**Pronto!** Isso resolve tudo automaticamente.

## 📋 O Que o Script Faz

1. ✅ Cria ambiente virtual (se não existir)
2. ✅ Instala pydantic com versão compatível (evita Rust)
3. ✅ Instala psycopg2-binary
4. ✅ Instala todas as outras dependências
5. ✅ Verifica se está tudo OK

**Tempo:** 2-5 minutos

## 🎯 Depois da Instalação

1. **Configure o .env:**
   ```cmd
   copy .env.example .env
   notepad .env
   ```

2. **Crie o banco de dados:**
   - Via pgAdmin: criar banco `financas_pessoais`
   - Ou: `psql -U postgres -c "CREATE DATABASE financas_pessoais;"`

3. **Execute migrations:**
   ```cmd
   python -m alembic upgrade head
   ```

4. **Inicie o servidor:**
   ```cmd
   python -m uvicorn app.main:app --reload --port 8000
   ```

## 📚 Mais Informações

- **Solução definitiva:** Veja `SOLUCAO_DEFINITIVA_RUST.md`
- **Verificar instalação:** Execute `verificar_instalacao.bat`
- **Outros problemas:** Veja `SOLUCAO_RAPIDA.md`

## 🆘 Ainda com Problemas?

Execute o script de verificação:

```cmd
verificar_instalacao.bat
```

Isso mostra exatamente o que está faltando.

---

**Resumo:** Execute `instalar_tudo_windows.bat` e pronto! 🎉

