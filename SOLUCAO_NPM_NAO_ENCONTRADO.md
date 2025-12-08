# 🔧 Solução: npm não encontrado

## ❌ O Problema

Você viu este erro:

```
❌ ERRO: npm não encontrado!
Instale Node.js de: https://nodejs.org/
```

## ✅ Soluções

### Solução 1: Instalar Node.js (Se Não Tiver)

1. **Baixe Node.js:**
   - Acesse: https://nodejs.org/
   - Baixe a versão LTS (recomendada)
   - Instale normalmente

2. **Reinicie o CMD** após instalar

3. **Verifique se funcionou:**
   ```cmd
   node --version
   npm --version
   ```

4. **Execute novamente:**
   ```cmd
   Iniciar_Sistema_MELHORADO.bat
   ```

### Solução 2: Verificar se Node.js Está no PATH

Se você já tem Node.js instalado mas não encontra:

1. **Encontre onde está instalado:**
   - Geralmente em: `C:\Program Files\nodejs\`
   - Ou: `C:\Program Files (x86)\nodejs\`

2. **Adicione ao PATH:**
   - Botão direito em "Este Computador" > Propriedades
   - Configurações avançadas do sistema
   - Variáveis de ambiente
   - Edite "Path" e adicione o caminho do Node.js

3. **Reinicie o CMD**

### Solução 3: Usar Script Melhorado

Use o script que verifica tudo antes:

```
Iniciar_Sistema_MELHORADO.bat
```

Este script:
- ✅ Verifica se npm está instalado
- ✅ Instala dependências do frontend automaticamente
- ✅ Dá mensagens de erro mais claras

## 🔍 Verificar Instalação

Execute este script para verificar tudo:

```cmd
verificar_requisitos.bat
```

Isso mostra exatamente o que está faltando.

## 📋 Checklist

- [ ] Node.js instalado? (`node --version`)
- [ ] npm instalado? (`npm --version`)
- [ ] Node.js no PATH?
- [ ] CMD reiniciado após instalar?

## 🚀 Depois de Instalar Node.js

1. **Verificar:**
   ```cmd
   node --version
   npm --version
   ```

2. **Instalar dependências do frontend:**
   ```cmd
   cd frontend
   npm install
   ```

3. **Iniciar sistema:**
   ```cmd
   Iniciar_Sistema_MELHORADO.bat
   ```

## 💡 Dica

**O npm vem junto com Node.js!**

Se você instalar Node.js, o npm será instalado automaticamente.

---

**Resumo:** Instale Node.js de https://nodejs.org/ e reinicie o CMD! 🚀

