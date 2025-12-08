@echo off
echo ========================================
echo  Configurar Backend para SQLite (Local)
echo ========================================
echo.

if not exist .env.local.example (
    echo ERRO: Arquivo .env.local.example nao encontrado!
    pause
    exit /b 1
)

if exist .env (
    echo Arquivo .env ja existe.
    echo.
    choice /C SN /M "Deseja sobrescrever com configuracao SQLite"
    if errorlevel 2 (
        echo Cancelado.
        pause
        exit /b 0
    )
)

echo Copiando configuracao SQLite...
copy .env.local.example .env
echo.
echo Arquivo .env criado com configuracao SQLite!
echo.
echo Configuracao:
echo - DATABASE_URL: sqlite:///./financas_pessoais.db
echo - DEBUG: true
echo - ENVIRONMENT: development
echo.
echo Deseja executar migrations agora?
choice /C SN /M "Executar migrations para criar o banco SQLite"
if errorlevel 2 (
    echo.
    echo OK. Execute depois: python -m alembic upgrade head
    pause
    exit /b 0
)

echo.
echo Executando migrations...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    python -m alembic upgrade head
    if errorlevel 1 (
        echo.
        echo ERRO ao executar migrations!
        echo Certifique-se de que o ambiente virtual esta ativado.
    ) else (
        echo.
        echo ✓ Migrations executadas com sucesso!
        echo Banco SQLite criado em: financas_pessoais.db
    )
) else (
    echo.
    echo AVISO: Ambiente virtual nao encontrado.
    echo Execute manualmente: python -m alembic upgrade head
)

echo.
echo ========================================
echo  Configuracao Concluida!
echo ========================================
echo.
echo Agora voce pode iniciar o servidor:
echo   python -m uvicorn app.main:app --reload --port 8000
echo.
pause

