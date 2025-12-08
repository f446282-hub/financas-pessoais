@echo off
echo ========================================
echo  Instalando SQLAlchemy
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

echo Instalando SQLAlchemy...
python -m pip install sqlalchemy==2.0.25

echo.
echo Verificando...
python -c "import sqlalchemy; print('✓ sqlalchemy instalado com sucesso!')" 2>nul
if errorlevel 1 (
    echo.
    echo Tentando versao mais recente...
    python -m pip install sqlalchemy
    python -c "import sqlalchemy; print('✓ sqlalchemy instalado!')" 2>nul
    if errorlevel 1 (
        echo.
        echo ERRO: Nao foi possivel instalar sqlalchemy
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo  SQLAlchemy instalado com sucesso!
echo ========================================
echo.
pause

