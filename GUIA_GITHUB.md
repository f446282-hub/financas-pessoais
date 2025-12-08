# 📤 Guia: Enviar Projeto para GitHub

Este guia mostra como enviar seu projeto Finanças Pessoais para o GitHub.

## 🎯 Pré-requisitos

1. **Conta no GitHub** (se não tiver, crie em: https://github.com)
2. **Git instalado** no seu computador
   - Verificar: `git --version`
   - Se não tiver: https://git-scm.com/downloads

## 🚀 Passo a Passo Completo

### 1. Criar Repositório no GitHub

1. **Acesse:** https://github.com
2. **Faça login** na sua conta
3. **Clique no botão "+"** (canto superior direito)
4. **Selecione "New repository"**
5. **Preencha:**
   - **Repository name:** `financas-pessoais` (ou o nome que preferir)
   - **Description:** "Sistema de gestão financeira pessoal"
   - **Visibilidade:** Público ou Privado (escolha)
   - **NÃO marque:** "Add a README file" (já temos)
   - **NÃO marque:** "Add .gitignore" (já temos)
   - **NÃO marque:** "Choose a license" (a menos que queira)
6. **Clique em "Create repository"**

### 2. Configurar Git Localmente

**Primeira vez usando Git neste computador:**

```cmd
git config --global user.name "Seu Nome"
git config --global user.email "seu-email@exemplo.com"
```

**Substitua pelos seus dados!**

### 3. Inicializar Git no Projeto

Execute na raiz do projeto:

```cmd
cd d:\financas-pessoais\financas-pessoais
git init
```

### 4. Adicionar Arquivos

```cmd
git add .
```

Isso adiciona todos os arquivos (respeitando o .gitignore)

### 5. Fazer Primeiro Commit

```cmd
git commit -m "Primeiro commit: Sistema Finanças Pessoais"
```

### 6. Conectar com GitHub

**Substitua `SEU_USUARIO` pelo seu nome de usuário do GitHub:**

```cmd
git remote add origin https://github.com/SEU_USUARIO/financas-pessoais.git
```

### 7. Enviar para GitHub

```cmd
git branch -M main
git push -u origin main
```

Você será solicitado a fazer login no GitHub.

## 📋 Comandos Rápidos (Copiar e Colar)

```cmd
REM 1. Configurar Git (primeira vez)
git config --global user.name "Seu Nome"
git config --global user.email "seu-email@exemplo.com"

REM 2. Inicializar repositório
cd d:\financas-pessoais\financas-pessoais
git init

REM 3. Adicionar arquivos
git add .

REM 4. Primeiro commit
git commit -m "Primeiro commit: Sistema Finanças Pessoais"

REM 5. Conectar com GitHub (substitua SEU_USUARIO)
git remote add origin https://github.com/SEU_USUARIO/financas-pessoais.git

REM 6. Enviar
git branch -M main
git push -u origin main
```

## 🔐 Autenticação no GitHub

### Opção 1: Personal Access Token (Recomendado)

1. **GitHub** > **Settings** > **Developer settings** > **Personal access tokens** > **Tokens (classic)**
2. **Generate new token (classic)**
3. **Selecione:** `repo` (acesso completo a repositórios)
4. **Gere o token** e copie
5. **Quando fizer push**, use o token como senha

### Opção 2: GitHub Desktop (Mais Fácil)

1. Instale: https://desktop.github.com/
2. Abra o GitHub Desktop
3. File > Add local repository
4. Selecione a pasta do projeto
5. Publish repository

## 📝 Script Automatizado

Criei um script que faz tudo automaticamente! Veja: `enviar_github.bat`

## 🔄 Atualizações Futuras

Depois do primeiro envio, para atualizar:

```cmd
git add .
git commit -m "Descrição das mudanças"
git push
```

## ✅ Checklist

- [ ] Conta no GitHub criada
- [ ] Git instalado (`git --version`)
- [ ] Repositório criado no GitHub
- [ ] Git configurado (`user.name` e `user.email`)
- [ ] Repositório inicializado (`git init`)
- [ ] Arquivos adicionados (`git add .`)
- [ ] Primeiro commit feito
- [ ] Conectado com GitHub (`git remote add`)
- [ ] Enviado para GitHub (`git push`)

## 🆘 Problemas Comuns

### Erro: "remote origin already exists"

**Solução:**
```cmd
git remote remove origin
git remote add origin https://github.com/SEU_USUARIO/financas-pessoais.git
```

### Erro: "failed to push"

**Solução:**
- Verifique se está logado no GitHub
- Use Personal Access Token como senha
- Ou use GitHub Desktop

### Erro: "permission denied"

**Solução:**
- Verifique o nome do repositório
- Verifique se você tem permissão
- Use HTTPS ao invés de SSH

## 📚 Recursos

- **GitHub Docs:** https://docs.github.com
- **Git Tutorial:** https://git-scm.com/docs
- **GitHub Desktop:** https://desktop.github.com/

---

**Pronto para enviar!** 🚀

