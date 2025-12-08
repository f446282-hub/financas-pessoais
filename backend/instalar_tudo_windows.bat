@echo off
echo ========================================
echo  Instalacao Completa - Windows (FIX Rust)
echo ========================================
echo.
echo Este script instala TUDO resolvendo o problema do Rust.
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    pause
    exit /b 1
)

REM Criar ambiente virtual se nao existir
if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ERRO: Falha ao criar ambiente virtual!
        pause
        exit /b 1
    )
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRO: Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)

echo.
echo [1/6] Atualizando pip, setuptools e wheel...
python -m pip install --upgrade pip setuptools wheel
echo.

echo [2/6] Instalando pydantic com versao compativel (evita Rust)...
echo.
python -m pip install "pydantic>=2.5.0,<2.6.0" "pydantic-settings>=2.0.0,<2.1.0" --prefer-binary
if errorlevel 1 (
    echo.
    echo Tentando versao mais antiga...
    python -m pip install "pydantic==2.5.3" "pydantic-settings==2.1.0" --prefer-binary
    if errorlevel 1 (
        echo.
        echo Tentando versao ainda mais compativel...
        python -m pip install "pydantic==2.4.2" "pydantic-settings==2.0.3" --prefer-binary
    )
)
echo.

echo [3/6] Verificando pydantic...
python -c "import pydantic; print('  ✓ pydantic OK')" 2>nul
if errorlevel 1 (
    echo   ✗ pydantic FALHOU
    echo.
    echo Execute: instalar_pydantic_fix.bat
    pause
    exit /b 1
)
echo.

echo [4/6] Instalando psycopg2-binary...
python -m pip install psycopg2-binary --no-cache-dir
if errorlevel 1 (
    echo.
    echo AVISO: Problema com psycopg2. Continuando...
)
echo.

echo [5/6] Instalando outras dependencias...
echo.
python -m pip install fastapi==0.109.2
python -m pip install "uvicorn[standard]==0.27.1"
python -m pip install python-multipart==0.0.9
python -m pip install sqlalchemy==2.0.25
if errorlevel 1 (
    echo   AVISO: Problema ao instalar sqlalchemy, tentando sem versao especifica...
    python -m pip install sqlalchemy
)
python -m pip install alembic==1.13.1
python -m pip install email-validator==2.1.0.post1
python -m pip install "python-jose[cryptography]==3.3.0"
python -m pip install "passlib[bcrypt]==1.7.4"
python -m pip install bcrypt==4.1.2
python -m pip install python-dotenv==1.0.1
python -m pip install httpx==0.26.0
python -m pip install pytest==8.0.0
python -m pip install pytest-asyncio==0.23.4
echo.

echo [6/6] Verificando instalacao final...
echo.
set ALL_OK=1

python -c "import pydantic; print('  ✓ pydantic: OK')" 2>nul || (echo   ✗ pydantic: FALHOU && set ALL_OK=0)
python -c "import psycopg2; print('  ✓ psycopg2: OK')" 2>nul || (echo   ✗ psycopg2: FALHOU && set ALL_OK=0)
python -c "import fastapi; print('  ✓ fastapi: OK')" 2>nul || (echo   ✗ fastapi: FALHOU && set ALL_OK=0)
python -c "import sqlalchemy; print('  ✓ sqlalchemy: OK')" 2>nul || (echo   ✗ sqlalchemy: FALHOU && set ALL_OK=0)

echo.
echo ========================================
if %ALL_OK%==1 (
    echo  ✓ INSTALACAO CONCLUIDA COM SUCESSO!
    echo ========================================
    echo.
    echo Todas as dependencias estao instaladas.
    echo Voce pode continuar com os proximos passos!
) else (
    echo  ⚠ INSTALACAO CONCLUIDA COM AVISOS
    echo ========================================
    echo.
    echo Algumas dependencias podem estar faltando.
    echo Veja os erros acima.
)
echo.
pause

