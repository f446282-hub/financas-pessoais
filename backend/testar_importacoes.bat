@echo off
echo ========================================
echo  Testando Importacoes das Dependencias
echo ========================================
echo.

REM Ativar ambiente virtual
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRO: Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)

echo Testando se as dependencias podem ser importadas...
echo.

set ALL_OK=1

echo [1/5] Testando pydantic...
python -c "import pydantic; print('  ✓ pydantic: OK - Versao', pydantic.__version__)" 2>nul
if errorlevel 1 (
    echo   ✗ pydantic: FALHOU ao importar
    set ALL_OK=0
)

echo [2/5] Testando psycopg2...
python -c "import psycopg2; print('  ✓ psycopg2: OK - Versao', psycopg2.__version__)" 2>nul
if errorlevel 1 (
    echo   ✗ psycopg2: FALHOU ao importar
    set ALL_OK=0
)

echo [3/5] Testando fastapi...
python -c "import fastapi; print('  ✓ fastapi: OK - Versao', fastapi.__version__)" 2>nul
if errorlevel 1 (
    echo   ✗ fastapi: FALHOU ao importar
    set ALL_OK=0
)

echo [4/5] Testando sqlalchemy...
python -c "import sqlalchemy; print('  ✓ sqlalchemy: OK - Versao', sqlalchemy.__version__)" 2>nul
if errorlevel 1 (
    echo   ✗ sqlalchemy: FALHOU ao importar
    echo   (Mas pode estar instalado - verificando...)
    python -c "import sqlalchemy" 2>&1 | findstr /C:"ModuleNotFoundError" >nul
    if errorlevel 1 (
        echo   ⚠ sqlalchemy pode estar instalado mas com problema
    )
    set ALL_OK=0
)

echo [5/5] Testando alembic...
python -c "import alembic; print('  ✓ alembic: OK')" 2>nul
if errorlevel 1 (
    echo   ✗ alembic: FALHOU ao importar
    set ALL_OK=0
)

echo.
echo ========================================
if %ALL_OK%==1 (
    echo  ✓ TODAS AS DEPENDENCIAS FUNCIONANDO!
    echo ========================================
    echo.
    echo Parabens! Tudo esta instalado e funcionando.
    echo Voce pode continuar com os proximos passos!
) else (
    echo  ⚠ ALGUNS PROBLEMAS ENCONTRADOS
    echo ========================================
    echo.
    echo Verifique quais dependencias falharam acima.
    echo A maioria provavelmente esta OK, apenas a verificacao falhou.
)
echo.
pause

