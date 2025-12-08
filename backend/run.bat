@echo off
echo ========================================
echo  Iniciando servidor FastAPI
echo ========================================
echo.

REM Verificar se o ambiente virtual existe
if not exist venv (
    echo ERRO: Ambiente virtual nao encontrado!
    echo Execute primeiro: setup_windows.bat
    pause
    exit /b 1
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRO: Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)

REM Verificar se .env existe
if not exist .env (
    echo AVISO: Arquivo .env nao encontrado!
    echo Copiando .env.example para .env...
    if exist .env.example (
        copy .env.example .env
        echo Arquivo .env criado! Configure-o antes de continuar.
        pause
        exit /b 1
    ) else (
        echo ERRO: Arquivo .env.example nao encontrado!
        pause
        exit /b 1
    )
)

echo.
echo Iniciando servidor na porta 8000...
echo Acesse: http://localhost:8000/docs
echo.
echo Pressione CTRL+C para parar o servidor.
echo.

python -m uvicorn app.main:app --reload --port 8000

