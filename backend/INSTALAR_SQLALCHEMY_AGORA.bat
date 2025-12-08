@echo off
echo ========================================
echo  Instalando SQLAlchemy (Dependencia Faltante)
echo ========================================
echo.

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
echo Verificando instalacao...
python -c "import sqlalchemy; print('✓ SQLAlchemy instalado com sucesso!'); print('Versao:', sqlalchemy.__version__)" 2>nul
if errorlevel 1 (
    echo.
    echo Tentando instalacao sem versao especifica...
    python -m pip install sqlalchemy
    python -c "import sqlalchemy; print('✓ SQLAlchemy instalado!')" 2>nul
    if errorlevel 1 (
        echo.
        echo ERRO: Nao foi possivel instalar SQLAlchemy
        echo Tente manualmente: python -m pip install sqlalchemy
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo  ✓ SQLAlchemy instalado!
echo ========================================
echo.
echo Execute agora: verificar_instalacao.bat
echo para verificar se tudo esta OK.
echo.
pause

