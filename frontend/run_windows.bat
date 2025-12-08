@echo off
echo ========================================
echo  Iniciando Frontend - Financas Pessoais
echo ========================================
echo.

REM Verificar se node_modules existe
if not exist node_modules (
    echo AVISO: Dependencias nao instaladas!
    echo.
    echo Execute primeiro: setup_windows.bat
    echo Ou: npm install
    echo.
    pause
    exit /b 1
)

REM Verificar se .env.local existe
if not exist .env.local (
    echo AVISO: Arquivo .env.local nao encontrado!
    echo.
    if exist .env.example (
        echo Copiando .env.example para .env.local...
        copy .env.example .env.local
    ) else (
        echo Criando .env.local basico...
        (
            echo NEXT_PUBLIC_API_URL=http://localhost:8000/api
            echo NEXT_PUBLIC_APP_NAME=Financas Pessoais
        ) > .env.local
    )
)

echo Iniciando servidor de desenvolvimento...
echo.
echo Frontend rodara em: http://localhost:3000
echo.
echo Pressione CTRL+C para parar o servidor.
echo.

npm run dev

