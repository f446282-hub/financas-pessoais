@echo off
echo ========================================
echo  Instalacao Fix - Pydantic (Evita Rust)
echo ========================================
echo.

REM Verificar ambiente virtual
if not exist venv (
    echo ERRO: Ambiente virtual nao encontrado!
    echo Execute primeiro: python -m venv venv
    pause
    exit /b 1
)

REM Ativar ambiente virtual
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRO: Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)

echo Atualizando pip, setuptools e wheel...
python -m pip install --upgrade pip setuptools wheel

echo.
echo ========================================
echo  Solucao 1: Instalando pydantic com binary wheels
echo ========================================
echo.

REM Tentar instalar usando apenas binary wheels
python -m pip install --only-binary :all: --prefer-binary pydantic pydantic-core pydantic-settings

python -c "import pydantic" 2>nul
if not errorlevel 1 (
    echo.
    echo ✓ SUCESSO! Pydantic instalado com binary wheels.
    goto :instalar_resto
)

echo.
echo ========================================
echo  Solucao 2: Instalando versao compativel
echo ========================================
echo.

REM Tentar instalar versao que tem wheels para Windows
python -m pip install "pydantic==2.5.3" "pydantic-core==2.14.6" "pydantic-settings==2.1.0"

python -c "import pydantic" 2>nul
if not errorlevel 1 (
    echo.
    echo ✓ SUCESSO! Pydantic instalado com versao compativel.
    goto :instalar_resto
)

echo.
echo ========================================
echo  Solucao 3: Instalando versao mais antiga garantida
echo ========================================
echo.

REM Instalar versao mais antiga que definitivamente tem wheels
python -m pip install "pydantic==2.4.2" "pydantic-settings==2.0.3"

python -c "import pydantic" 2>nul
if not errorlevel 1 (
    echo.
    echo ✓ SUCESSO! Pydantic instalado com versao compativel.
    goto :instalar_resto
)

echo.
echo ========================================
echo  ERRO: Nao foi possivel instalar pydantic
echo ========================================
echo.
echo SOLUCAO ALTERNATIVA:
echo.
echo 1. Instale o Rust (opcional, mas resolve definitivamente):
echo    https://rustup.rs/
echo.
echo 2. Ou use uma versao diferente do Python (3.10 ou 3.11)
echo.
echo 3. Ou edite requirements.txt para usar versao mais antiga:
echo    pydantic==2.4.2
echo.
pause
exit /b 1

:instalar_resto
echo.
echo ========================================
echo  Instalando outras dependencias
echo ========================================
echo.

REM Instalar outras dependencias (ignorando pydantic no requirements)
python -m pip install fastapi uvicorn sqlalchemy alembic python-jose passlib bcrypt python-dotenv httpx pytest pytest-asyncio python-multipart email-validator psycopg2-binary

echo.
echo ========================================
echo  Verificando instalacao
echo ========================================
echo.

python -c "import pydantic; print('✓ pydantic: OK')" 2>nul
python -c "import psycopg2; print('✓ psycopg2: OK')" 2>nul
python -c "import fastapi; print('✓ fastapi: OK')" 2>nul

echo.
echo ========================================
echo  Instalacao Concluida!
echo ========================================
echo.
pause

