# ⚡ Solução Rápida - Problemas de Instalação no Windows

## 🚨 Erros Comuns e Soluções Imediatas

### Erro 1: pydantic-core (Rust)

**Sintoma:**
```
Cargo, the Rust package manager, is not installed
error: metadata-generation-failed
╰─> pydantic-core
```

**Solução Rápida:**
```cmd
venv\Scripts\activate.bat
python -m pip install --only-binary :all: pydantic pydantic-core pydantic-settings
python -m pip install -r requirements.txt
```

**Ou use o script:**
```cmd
install_dependencies_windows.bat
```

---

### Erro 2: psycopg2-binary

**Sintoma:**
```
ERROR: Failed to build 'psycopg2-binary'
```

**Solução Rápida:**
```cmd
install_psycopg2_windows.bat
```

**Ou veja:** `SOLUCAO_PSYCOPG2.md`

---

### Erro 3: Múltiplos Erros

**Solução Completa Automatizada:**

```cmd
install_dependencies_windows.bat
```

Este script resolve automaticamente:
- ✅ Problemas com pydantic (Rust)
- ✅ Problemas com psycopg2-binary
- ✅ Outras dependências

---

## 🎯 Solução Definitiva (Recomendado)

Execute este script que faz tudo automaticamente:

```cmd
install_dependencies_windows.bat
```

**Este script:**
1. ✅ Ativa o ambiente virtual
2. ✅ Atualiza pip, setuptools, wheel
3. ✅ Instala pydantic com binary wheels (evita Rust)
4. ✅ Instala psycopg2-binary
5. ✅ Instala todas as outras dependências
6. ✅ Verifica se tudo está OK

---

## 📋 Comandos Manuais (Se Precisar)

Se o script automático não funcionar, execute na ordem:

```cmd
REM 1. Ativar ambiente virtual
venv\Scripts\activate.bat

REM 2. Atualizar ferramentas
python -m pip install --upgrade pip setuptools wheel

REM 3. Instalar pydantic (evita Rust)
python -m pip install --only-binary :all: pydantic pydantic-core pydantic-settings

REM 4. Instalar psycopg2
python -m pip install psycopg2-binary --no-cache-dir

REM 5. Instalar resto
python -m pip install -r requirements.txt
```

---

## 🔍 Verificar se Funcionou

Após instalar, teste:

```cmd
python -c "import pydantic; print('OK - pydantic')"
python -c "import psycopg2; print('OK - psycopg2')"
python -c "import fastapi; print('OK - fastapi')"
```

Se todos mostrarem "OK", está funcionando!

---

## 📚 Documentação Completa

- **pydantic:** `SOLUCAO_PYDANTIC.md`
- **psycopg2:** `SOLUCAO_PSYCOPG2.md`
- **Geral:** `README.md`

---

## 🆘 Ainda com Problemas?

1. Verifique a versão do Python: `python --version` (precisa ser 3.11+)
2. Certifique-se de que o ambiente virtual está ativado
3. Tente em um novo ambiente virtual:
   ```cmd
   python -m venv venv_novo
   venv_novo\Scripts\activate.bat
   install_dependencies_windows.bat
   ```

---

**Última atualização:** 2024

