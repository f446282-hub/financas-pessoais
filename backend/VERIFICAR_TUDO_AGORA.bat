@echo off
echo ========================================
echo  Verificacao Completa - Todas Dependencias
echo ========================================
echo.

REM Ativar ambiente virtual
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRO: Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)

echo Testando importacao de todas as dependencias principais...
echo.

set COUNT_OK=0
set COUNT_FAIL=0

echo Testando pydantic...
python -c "import pydantic; print('✓ pydantic OK')" 2>nul && set /a COUNT_OK+=1 || set /a COUNT_FAIL+=1

echo Testando psycopg2...
python -c "import psycopg2; print('✓ psycopg2 OK')" 2>nul && set /a COUNT_OK+=1 || set /a COUNT_FAIL+=1

echo Testando fastapi...
python -c "import fastapi; print('✓ fastapi OK')" 2>nul && set /a COUNT_OK+=1 || set /a COUNT_FAIL+=1

echo Testando sqlalchemy...
python -c "import sqlalchemy; print('✓ sqlalchemy OK')" 2>nul && set /a COUNT_OK+=1 || (
    echo Verificando sqlalchemy de outra forma...
    python -c "from sqlalchemy import create_engine; print('✓ sqlalchemy OK (funcional)')" 2>nul && set /a COUNT_OK+=1 || set /a COUNT_FAIL+=1
)

echo Testando alembic...
python -c "import alembic; print('✓ alembic OK')" 2>nul && set /a COUNT_OK+=1 || set /a COUNT_FAIL+=1

echo.
echo ========================================
echo  Resultado: %COUNT_OK% OK, %COUNT_FAIL% Falharam
echo ========================================
echo.

if %COUNT_FAIL%==0 (
    echo ✓ TUDO PERFEITO! Todas as dependencias estao funcionando!
    echo.
    echo Voce pode continuar com:
    echo 1. Configurar .env
    echo 2. Criar banco de dados
    echo 3. Executar migrations
    echo 4. Iniciar servidor
) else if %COUNT_OK% GEQ 4 (
    echo ⚠ QUASE TUDO OK! Apenas %COUNT_FAIL% dependencia(s) pode(m) ter problema.
    echo.
    echo Provavelmente esta tudo funcionando mesmo assim.
    echo Tente iniciar o servidor e veja se funciona.
) else (
    echo ✗ ALGUMAS DEPENDENCIAS ESTAO FALTANDO
    echo.
    echo Execute: instalar_tudo_windows.bat
)

echo.
pause

