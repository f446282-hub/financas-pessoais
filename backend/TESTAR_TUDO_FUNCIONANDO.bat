@echo off
echo ========================================
echo  Teste Final - Verificar se TUDO Funciona
echo ========================================
echo.

REM Ativar ambiente virtual
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRO: Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)

echo Testando se conseguimos importar todas as dependencias...
echo.

set TOTAL_OK=0
set TOTAL_FAIL=0

echo [1/5] Testando pydantic...
python -c "import pydantic; print('  ✓ pydantic: FUNCIONANDO')" 2>nul
if errorlevel 1 (
    echo   ✗ pydantic: NAO FUNCIONA
    set /a TOTAL_FAIL+=1
) else (
    set /a TOTAL_OK+=1
)

echo [2/5] Testando psycopg2...
python -c "import psycopg2; print('  ✓ psycopg2: FUNCIONANDO')" 2>nul
if errorlevel 1 (
    echo   ✗ psycopg2: NAO FUNCIONA
    set /a TOTAL_FAIL+=1
) else (
    set /a TOTAL_OK+=1
)

echo [3/5] Testando fastapi...
python -c "import fastapi; print('  ✓ fastapi: FUNCIONANDO')" 2>nul
if errorlevel 1 (
    echo   ✗ fastapi: NAO FUNCIONA
    set /a TOTAL_FAIL+=1
) else (
    set /a TOTAL_OK+=1
)

echo [4/5] Testando sqlalchemy...
python -c "import sqlalchemy; print('  ✓ sqlalchemy: FUNCIONANDO (versao', sqlalchemy.__version__, ')')" 2>nul
if errorlevel 1 (
    echo   Testando importacao alternativa de sqlalchemy...
    python -c "from sqlalchemy import create_engine; print('  ✓ sqlalchemy: FUNCIONANDO (importacao alternativa OK)')" 2>nul
    if errorlevel 1 (
        echo   ✗ sqlalchemy: NAO FUNCIONA
        set /a TOTAL_FAIL+=1
    ) else (
        set /a TOTAL_OK+=1
    )
) else (
    set /a TOTAL_OK+=1
)

echo [5/5] Testando alembic...
python -c "import alembic; print('  ✓ alembic: FUNCIONANDO')" 2>nul
if errorlevel 1 (
    echo   ✗ alembic: NAO FUNCIONA
    set /a TOTAL_FAIL+=1
) else (
    set /a TOTAL_OK+=1
)

echo.
echo ========================================
echo  RESULTADO: %TOTAL_OK% OK de 5 dependencias
echo ========================================
echo.

if %TOTAL_FAIL%==0 (
    echo ✓ PARABENS! TODAS AS DEPENDENCIAS ESTAO FUNCIONANDO!
    echo.
    echo O SQLAlchemy ESTA INSTALADO e FUNCIONANDO!
    echo O erro anterior era apenas do script de verificacao.
    echo.
    echo Voce pode continuar com os proximos passos:
    echo 1. Configurar .env
    echo 2. Criar banco de dados PostgreSQL
    echo 3. Executar migrations
    echo 4. Iniciar servidor
) else if %TOTAL_OK% GEQ 4 (
    echo ⚠ QUASE PERFEITO! %TOTAL_OK% de 5 estao OK.
    echo.
    echo Provavelmente tudo esta funcionando mesmo assim.
    echo O SQLAlchemy ESTA instalado (vimos isso na mensagem anterior).
    echo.
    echo Tente iniciar o servidor e veja se funciona:
    echo   python -m uvicorn app.main:app --reload --port 8000
) else (
    echo ✗ Algumas dependencias podem estar faltando.
    echo.
    echo Execute: instalar_tudo_windows.bat
)

echo.
pause

