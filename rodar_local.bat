@echo off
echo ========================================
echo  Iniciar Sistema Local - SQLite
echo ========================================
echo.
echo Este script ira:
echo 1. Configurar SQLite automaticamente
echo 2. Iniciar Backend (porta 8000)
echo 3. Iniciar Frontend (porta 3000)
echo 4. Abrir navegador
echo.
pause

set BACKEND_DIR=backend
set FRONTEND_DIR=frontend

REM Verificar se estamos na raiz
if not exist %BACKEND_DIR% (
    echo ERRO: Execute este script da raiz do projeto!
    pause
    exit /b 1
)

REM Configurar Backend para SQLite
echo.
echo [1/4] Configurando Backend para SQLite...
cd %BACKEND_DIR%

if not exist .env (
    if exist .env.example (
        copy .env.example .env
    ) else (
        echo DATABASE_URL=sqlite:///./financas_pessoais.db > .env
        echo SECRET_KEY=local-development-key-change-in-production >> .env
        echo DEBUG=true >> .env
        echo ENVIRONMENT=development >> .env
    )
)

REM Verificar se DATABASE_URL já está configurado para SQLite
findstr /C:"sqlite" .env >nul
if errorlevel 1 (
    echo Configurando DATABASE_URL para SQLite...
    (
        echo DATABASE_URL=sqlite:///./financas_pessoais.db
        echo SECRET_KEY=local-development-key-change-in-production
        echo DEBUG=true
        echo ENVIRONMENT=development
    ) > .env.local
    echo Arquivo .env.local criado com configuracao SQLite!
    echo.
    echo IMPORTANTE: Verifique o arquivo .env e ajuste se necessario.
    echo Se quiser usar .env.local, copie para .env
    echo.
)

REM Ativar venv e verificar migrations
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Verificando se migrations foram executadas...
    if not exist financas_pessoais.db (
        echo Banco SQLite nao encontrado. Executando migrations...
        python -m alembic upgrade head
    )
)

cd ..

REM Iniciar Backend
echo.
echo [2/4] Iniciando Backend...
cd %BACKEND_DIR%
if exist venv\Scripts\activate.bat (
    start "Backend - Financas Pessoais (SQLite)" /D %CD% cmd /k "venv\Scripts\activate.bat && python -m uvicorn app.main:app --reload --port 8000"
) else (
    start "Backend - Financas Pessoais (SQLite)" /D %CD% cmd /k "python -m uvicorn app.main:app --reload --port 8000"
)

cd ..

REM Aguardar backend iniciar
echo Aguardando backend iniciar...
timeout /t 3 /nobreak >nul

REM Verificar Frontend
echo.
echo [3/4] Verificando Frontend...
cd %FRONTEND_DIR%

if not exist node_modules (
    echo Dependencias do frontend nao instaladas!
    echo Execute primeiro: cd frontend && setup_windows.bat
    echo.
    pause
    exit /b 1
)

cd ..

REM Iniciar Frontend
echo.
echo [4/4] Iniciando Frontend...
cd %FRONTEND_DIR%
start "Frontend - Financas Pessoais" /D %CD% cmd /k "npm run dev"

cd ..

REM Aguardar frontend iniciar
echo Aguardando frontend iniciar...
timeout /t 5 /nobreak >nul

REM Abrir navegador
echo.
echo Abrindo navegador...
start http://localhost:3000

echo.
echo ========================================
echo  Sistema Iniciado!
echo ========================================
echo.
echo - Backend: http://localhost:8000/docs
echo - Frontend: http://localhost:3000
echo.
echo Banco de dados: SQLite (backend/financas_pessoais.db)
echo.
echo Para encerrar, feche as janelas do Backend e Frontend.
echo.
pause

