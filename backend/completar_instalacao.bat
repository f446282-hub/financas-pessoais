@echo off
echo ========================================
echo  Completar Instalacao - Dependencias Faltantes
echo ========================================
echo.

REM Verificar ambiente virtual
if not exist venv (
    echo ERRO: Ambiente virtual nao encontrado!
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

echo Instalando dependencias faltantes...
echo.

echo [1/4] Instalando SQLAlchemy...
python -m pip install sqlalchemy==2.0.25
python -c "import sqlalchemy; print('  ✓ SQLAlchemy: OK')" 2>nul || echo   ✗ SQLAlchemy: FALHOU

echo.
echo [2/4] Instalando outras dependencias que podem estar faltando...
python -m pip install alembic==1.13.1
python -c "import alembic; print('  ✓ Alembic: OK')" 2>nul || echo   ✗ Alembic: FALHOU

echo.
echo [3/4] Instalando utilitarios...
python -m pip install python-dotenv==1.0.1
python -m pip install httpx==0.26.0
python -m pip install email-validator==2.1.0.post1

echo.
echo [4/4] Verificando instalacao completa...
echo.

set ALL_OK=1

python -c "import pydantic; print('  ✓ pydantic: OK')" 2>nul || (echo   ✗ pydantic: FALHOU && set ALL_OK=0)
python -c "import psycopg2; print('  ✓ psycopg2: OK')" 2>nul || (echo   ✗ psycopg2: FALHOU && set ALL_OK=0)
python -c "import fastapi; print('  ✓ fastapi: OK')" 2>nul || (echo   ✗ fastapi: FALHOU && set ALL_OK=0)
python -c "import sqlalchemy; print('  ✓ sqlalchemy: OK')" 2>nul || (echo   ✗ sqlalchemy: FALHOU && set ALL_OK=0)
python -c "import alembic; print('  ✓ alembic: OK')" 2>nul || (echo   ✗ alembic: FALHOU && set ALL_OK=0)

echo.
echo ========================================
if %ALL_OK%==1 (
    echo  ✓ TODAS AS DEPENDENCIAS ESTAO OK!
    echo ========================================
    echo.
    echo Instalacao completa! Voce pode continuar.
) else (
    echo  ⚠ ALGUMAS DEPENDENCIAS AINDA FALTANDO
    echo ========================================
    echo.
    echo Veja quais falharam acima e tente instalar manualmente:
    echo   python -m pip install nome_da_dependencia
)
echo.
pause

