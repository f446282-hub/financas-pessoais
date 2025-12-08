# 🔧 Solução para Erro do pydantic-core (Rust)

## ❌ Erro Comum

```
Cargo, the Rust package manager, is not installed or is not on PATH.
error: metadata-generation-failed
× Encountered error while generating package metadata.
╰─> pydantic-core
```

## 🎯 Solução Rápida

O `pydantic-core` precisa compilar extensões Rust. Vamos usar wheels pré-compilados!

### Opção 1: Instalar com Binary Wheels (Mais Fácil)

Execute este comando:

```cmd
venv\Scripts\activate.bat
python -m pip install --only-binary :all: pydantic pydantic-core pydantic-settings
python -m pip install -r requirements.txt
```

### Opção 2: Instalar Rust (Se quiser compilar)

1. **Baixe e instale o Rust:**
   - Acesse: https://rustup.rs/
   - Baixe e execute o instalador
   - Reinicie o CMD após instalar

2. **Depois execute:**
   ```cmd
   venv\Scripts\activate.bat
   python -m pip install -r requirements.txt
   ```

### Opção 3: Usar Versão Mais Antiga (Compatível)

Atualize o `requirements.txt` para usar versões com wheels pré-compilados:

```txt
pydantic>=2.0.0,<2.6.0
pydantic-settings>=2.0.0,<2.1.0
```

## 🚀 Script Automatizado (RECOMENDADO)

Use o script que resolve TUDO automaticamente:

```cmd
instalar_tudo_windows.bat
```

Este script:
- ✅ Instala pydantic com versão compatível (evita Rust)
- ✅ Instala todas as outras dependências
- ✅ Verifica se tudo está OK

**OU** use o script específico para pydantic:

```cmd
instalar_pydantic_fix.bat
```

Este script tenta 3 soluções diferentes até funcionar.

## ⚡ Solução Rápida (Copiar e Colar)

Execute estes comandos na ordem:

```cmd
REM Ativar ambiente virtual
venv\Scripts\activate.bat

REM Atualizar pip e ferramentas
python -m pip install --upgrade pip setuptools wheel

REM Instalar pydantic com binary wheels
python -m pip install --only-binary :all: pydantic pydantic-core pydantic-settings

REM Instalar outras dependências
python -m pip install -r requirements.txt
```

## 🔍 Verificar Instalação

Após instalar, verifique:

```cmd
python -c "import pydantic; print('OK!')"
```

Se mostrar "OK!", está funcionando!

## 📝 Notas

- Wheels pré-compilados são mais rápidos e não precisam de Rust
- A instalação do Rust é opcional, apenas se quiser compilar do zero
- O problema é comum no Windows com Python 3.11+

## 🆘 Ainda com Problemas?

1. Verifique a versão do Python: `python --version`
2. Certifique-se de usar Python 3.11+
3. Tente instalar versão específica: `pip install pydantic==2.5.0`
4. Veja logs completos do erro para mais detalhes

