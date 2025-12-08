@echo off
REM Launcher melhorado com verificacoes completas
title Financas Pessoais - Iniciando Sistema...

echo.
echo ========================================
echo   💰 Financas Pessoais
echo   Iniciando Sistema Completo...
echo ========================================
echo.

cd /d "%~dp0"
set ROOT_DIR=%~dp0

REM Verificar requisitos basicos
echo Verificando requisitos...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python 3.11+ de: https://www.python.org/
    pause
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Node.js nao encontrado!
    echo Instale Node.js 18+ de: https://nodejs.org/
    pause
    exit /b 1
)

npm --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: npm nao encontrado!
    echo (Geralmente vem com Node.js - reinstale Node.js)
    pause
    exit /b 1
)

echo ✓ Requisitos basicos OK!
echo.

REM Verificar diretorios
if not exist "%ROOT_DIR%backend" (
    echo ERRO: Pasta backend nao encontrada em: %ROOT_DIR%
    pause
    exit /b 1
)

if not exist "%ROOT_DIR%frontend" (
    echo ERRO: Pasta frontend nao encontrada em: %ROOT_DIR%
    pause
    exit /b 1
)

REM Configurar Backend para SQLite se necessario
if not exist "%ROOT_DIR%backend\.env" (
    echo [1/6] Configurando backend para SQLite...
    (
        echo DATABASE_URL=sqlite:///./financas_pessoais.db
        echo SECRET_KEY=local-development-key-change-in-production-12345
        echo DEBUG=true
        echo ENVIRONMENT=development
        echo CORS_ORIGINS=["http://localhost:3000"]
        echo ALGORITHM=HS256
        echo ACCESS_TOKEN_EXPIRE_MINUTES=1440
    ) > "%ROOT_DIR%backend\.env"
    echo    ✓ Configuracao criada!
) else (
    echo [1/6] Configuracao do backend encontrada.
)

REM Verificar e executar migrations
if not exist "%ROOT_DIR%backend\financas_pessoais.db" (
    echo.
    echo [2/6] Executando migrations (cria banco SQLite)...
    cd "%ROOT_DIR%backend"
    if exist "venv\Scripts\activate.bat" (
        call venv\Scripts\activate.bat
        echo    Executando: python -m alembic upgrade head
        python -m alembic upgrade head
        if errorlevel 1 (
            echo.
            echo    ⚠ AVISO: Migrations falharam!
            echo    Mas vamos continuar - o banco sera criado automaticamente.
            echo    Se houver problemas, execute manualmente:
            echo      cd backend
            echo      venv\Scripts\activate.bat
            echo      python -m alembic upgrade head
        ) else (
            echo    ✓ Banco SQLite criado!
        )
    ) else (
        echo    ⚠ AVISO: Ambiente virtual nao encontrado!
        echo    Execute primeiro: cd backend ^&^& python -m venv venv
    )
    cd "%ROOT_DIR%"
) else (
    echo [2/6] Banco SQLite encontrado.
)

REM Verificar dependencias do frontend
echo.
echo [3/6] Verificando dependencias do frontend...
cd "%ROOT_DIR%frontend"
if not exist "node_modules" (
    echo    ⚠ Dependencias nao encontradas!
    echo    Instalando dependencias do frontend...
    echo    (Isso pode demorar alguns minutos na primeira vez)
    echo.
    npm install
    if errorlevel 1 (
        echo.
        echo    ⚠ ERRO: Falha ao instalar dependencias do frontend!
        echo    Tente manualmente: cd frontend ^&^& npm install
        echo    Continuando mesmo assim...
    ) else (
        echo    ✓ Dependencias do frontend instaladas!
    )
) else (
    echo    ✓ Dependencias do frontend encontradas!
)
cd "%ROOT_DIR%"

REM Iniciar Backend
echo.
echo [4/6] Iniciando Backend...
cd "%ROOT_DIR%backend"
if exist "venv\Scripts\activate.bat" (
    start "Backend - Financas Pessoais" /MIN cmd /k "cd /d %ROOT_DIR%backend && venv\Scripts\activate.bat && python -m uvicorn app.main:app --reload --port 8000"
) else (
    echo    ⚠ AVISO: Ambiente virtual nao encontrado!
    echo    Iniciando sem venv (pode nao funcionar)...
    start "Backend - Financas Pessoais" /MIN cmd /k "cd /d %ROOT_DIR%backend && python -m uvicorn app.main:app --reload --port 8000"
)
cd "%ROOT_DIR%"

REM Aguardar backend iniciar
echo    Aguardando backend iniciar...
timeout /t 5 /nobreak >nul

REM Iniciar Frontend
echo.
echo [5/6] Iniciando Frontend...
cd "%ROOT_DIR%frontend"
start "Frontend - Financas Pessoais" /MIN cmd /k "cd /d %ROOT_DIR%frontend && npm run dev"
cd "%ROOT_DIR%"

REM Aguardar frontend iniciar
echo    Aguardando frontend iniciar...
timeout /t 8 /nobreak >nul

REM Abrir navegador
echo.
echo [6/6] Abrindo navegador...
start http://localhost:3000

echo.
echo ========================================
echo   ✅ Sistema Iniciado!
echo ========================================
echo.
echo 📍 Acesse:
echo    - Frontend: http://localhost:3000
echo    - Backend API: http://localhost:8000/docs
echo.
echo 💡 Para encerrar, feche as janelas do Backend e Frontend
echo.
pause

