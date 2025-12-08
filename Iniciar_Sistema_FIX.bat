@echo off
REM Launcher melhorado que sempre encontra os diretorios corretos
title Financas Pessoais - Iniciando Sistema...

echo.
echo ========================================
echo   💰 Financas Pessoais
echo   Iniciando Sistema Completo...
echo ========================================
echo.

REM Sempre usar o diretorio onde o script esta
cd /d "%~dp0"
set ROOT_DIR=%~dp0

echo Diretorio base: %ROOT_DIR%
echo.

REM Verificar diretorios usando caminho completo
if not exist "%ROOT_DIR%backend" (
    echo ERRO: Pasta backend nao encontrada em: %ROOT_DIR%
    echo.
    echo Verificando diretorio atual...
    cd
    echo Diretorio atual: %CD%
    echo.
    echo Procurando pasta backend...
    dir /b /ad | findstr /i backend
    if errorlevel 1 (
        echo Backend nao encontrado no diretorio atual.
    )
    echo.
    pause
    exit /b 1
)

if not exist "%ROOT_DIR%frontend" (
    echo ERRO: Pasta frontend nao encontrada em: %ROOT_DIR%
    pause
    exit /b 1
)

echo ✓ Pastas backend e frontend encontradas!
echo.

REM Voltar para o diretorio raiz
cd /d "%ROOT_DIR%"

REM Configurar Backend para SQLite se necessario
if not exist "%ROOT_DIR%backend\.env" (
    echo [1/5] Configurando backend para SQLite...
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
    echo [1/5] Configuracao do backend encontrada.
)

REM Verificar migrations
if not exist "%ROOT_DIR%backend\financas_pessoais.db" (
    echo.
    echo [2/5] Executando migrations (cria banco SQLite)...
    cd "%ROOT_DIR%backend"
    if exist "venv\Scripts\activate.bat" (
        call venv\Scripts\activate.bat
        python -m alembic upgrade head >nul 2>&1
        if errorlevel 1 (
            echo    ⚠ Aviso: Nao foi possivel executar migrations automaticamente.
            echo    Execute manualmente depois se necessario.
        ) else (
            echo    ✓ Banco SQLite criado!
        )
    )
    cd "%ROOT_DIR%"
) else (
    echo [2/5] Banco SQLite encontrado.
)

REM Iniciar Backend
echo.
echo [3/5] Iniciando Backend...
cd "%ROOT_DIR%backend"
if exist "venv\Scripts\activate.bat" (
    start "Backend - Financas Pessoais" /MIN cmd /k "cd /d %ROOT_DIR%backend && venv\Scripts\activate.bat && python -m uvicorn app.main:app --reload --port 8000"
) else (
    start "Backend - Financas Pessoais" /MIN cmd /k "cd /d %ROOT_DIR%backend && python -m uvicorn app.main:app --reload --port 8000"
)
cd "%ROOT_DIR%"

REM Aguardar backend iniciar
echo    Aguardando backend iniciar...
timeout /t 5 /nobreak >nul

REM Verificar Frontend
echo.
echo [4/5] Verificando Frontend...
cd "%ROOT_DIR%frontend"
if not exist "node_modules" (
    echo    ⚠ AVISO: Dependencias do frontend nao encontradas!
    echo    Execute primeiro: cd frontend ^&^& setup_windows.bat
    echo    Continuando mesmo assim...
)
cd "%ROOT_DIR%"

REM Iniciar Frontend
echo.
echo [5/5] Iniciando Frontend...
cd "%ROOT_DIR%frontend"
start "Frontend - Financas Pessoais" /MIN cmd /k "cd /d %ROOT_DIR%frontend && npm run dev"
cd "%ROOT_DIR%"

REM Aguardar frontend iniciar
echo    Aguardando frontend iniciar...
timeout /t 8 /nobreak >nul

REM Abrir navegador
echo.
echo Abrindo navegador...
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
echo    ou pressione qualquer tecla aqui para mostrar as janelas.
echo.
pause

echo.
echo Sistema rodando! Feche esta janela quando quiser.
pause

