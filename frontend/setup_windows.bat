@echo off
echo ========================================
echo  Instalacao do Frontend - Windows
echo ========================================
echo.

REM Verificar Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Node.js nao encontrado!
    echo.
    echo Instale Node.js 18+ de: https://nodejs.org/
    pause
    exit /b 1
)

echo Node.js encontrado!
node --version
echo.

REM Verificar npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: npm nao encontrado!
    pause
    exit /b 1
)

echo npm encontrado!
npm --version
echo.

echo [1/3] Instalando dependencias...
echo (Isso pode demorar alguns minutos na primeira vez)
echo.
npm install
if errorlevel 1 (
    echo.
    echo ERRO: Falha ao instalar dependencias!
    echo.
    echo Tente:
    echo 1. Limpar cache: npm cache clean --force
    echo 2. Deletar node_modules e package-lock.json
    echo 3. Executar npm install novamente
    pause
    exit /b 1
)

echo.
echo [2/3] Copiando arquivo .env...
if exist .env.local (
    echo Arquivo .env.local ja existe. Pulando...
) else (
    if exist .env.example (
        copy .env.example .env.local
        echo Arquivo .env.local criado!
    ) else (
        echo AVISO: Arquivo .env.example nao encontrado!
        echo Criando .env.local basico...
        (
            echo NEXT_PUBLIC_API_URL=http://localhost:8000/api
            echo NEXT_PUBLIC_APP_NAME=Financas Pessoais
        ) > .env.local
        echo Arquivo .env.local criado com valores padrao!
    )
)

echo.
echo [3/3] Configuracao concluida!
echo.
echo ========================================
echo  PROXIMOS PASSOS:
echo ========================================
echo.
echo 1. Configure o arquivo .env.local se necessario:
echo    notepad .env.local
echo.
echo 2. Inicie o servidor de desenvolvimento:
echo    npm run dev
echo.
echo    Ou use o script: run_windows.bat
echo.
echo Acesse: http://localhost:3000
echo.
echo ========================================
pause

