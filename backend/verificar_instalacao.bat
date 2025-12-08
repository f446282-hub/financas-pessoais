@echo off
echo ========================================
echo  Verificacao de Instalacao
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

echo Verificando dependencias instaladas...
echo.

set ALL_OK=1

echo [1/5] Verificando pydantic...
python -c "import pydantic; print('  ✓ pydantic: OK'); exit(0)" 2>nul
if errorlevel 1 (
    echo   ✗ pydantic: NAO INSTALADO
    set ALL_OK=0
)

echo [2/5] Verificando psycopg2...
python -c "import psycopg2; print('  ✓ psycopg2: OK'); exit(0)" 2>nul
if errorlevel 1 (
    echo   ✗ psycopg2: NAO INSTALADO
    set ALL_OK=0
)

echo [3/5] Verificando fastapi...
python -c "import fastapi; print('  ✓ fastapi: OK'); exit(0)" 2>nul
if errorlevel 1 (
    echo   ✗ fastapi: NAO INSTALADO
    set ALL_OK=0
)

echo [4/5] Verificando sqlalchemy...
python -c "import sqlalchemy; print('  ✓ sqlalchemy: OK'); exit(0)" 2>nul
if errorlevel 1 (
    echo   ✗ sqlalchemy: NAO INSTALADO
    set ALL_OK=0
)

echo [5/5] Verificando alembic...
python -c "import alembic; print('  ✓ alembic: OK'); exit(0)" 2>nul
if errorlevel 1 (
    echo   ✗ alembic: NAO INSTALADO
    set ALL_OK=0
)

echo.
echo ========================================
if %ALL_OK%==1 (
    echo  ✓ TODAS AS DEPENDENCIAS ESTAO OK!
    echo ========================================
    echo.
    echo Voce pode continuar com os proximos passos:
    echo 1. Configurar .env
    echo 2. Criar banco de dados
    echo 3. Executar migrations
    echo 4. Iniciar servidor
) else (
    echo  ⚠ ALGUMAS DEPENDENCIAS FALTANDO
    echo ========================================
    echo.
    echo Execute para instalar:
    echo   install_dependencies_windows.bat
    echo.
    echo Ou veja:
    echo   ESTA_TUDO_OK.md
)
echo.
pause

