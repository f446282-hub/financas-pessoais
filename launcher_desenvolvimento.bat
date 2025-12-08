@echo off
REM Launcher para desenvolvimento - inicia backend e frontend
echo ========================================
echo  Financas Pessoais - Modo Desenvolvimento
echo ========================================
echo.

REM Verificar se estamos no diretorio correto
if not exist backend (
    echo ERRO: Execute este script da raiz do projeto!
    pause
    exit /b 1
)

REM Iniciar Backend
echo [1/2] Iniciando Backend...
start "Backend - Financas Pessoais" /D backend cmd /k "venv\Scripts\activate.bat && python -m uvicorn app.main:app --reload --port 8000"

REM Aguardar backend iniciar
echo Aguardando backend iniciar...
timeout /t 3 /nobreak >nul

REM Iniciar Frontend
echo [2/2] Iniciando Frontend...
start "Frontend - Financas Pessoais" /D frontend cmd /k "npm run dev"

REM Aguardar frontend iniciar
echo Aguardando frontend iniciar...
timeout /t 5 /nobreak >nul

REM Abrir navegador
echo.
echo Abrindo navegador...
start http://localhost:3000

echo.
echo ========================================
echo  Sistema iniciado!
echo ========================================
echo.
echo - Backend: http://localhost:8000/docs
echo - Frontend: http://localhost:3000
echo.
echo Para encerrar, feche as janelas do Backend e Frontend
echo ou pressione CTRL+C aqui.
echo.
pause

