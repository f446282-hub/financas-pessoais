@echo off
echo ========================================
echo  Build Completo - Financas Pessoais
echo ========================================
echo.
echo Este script ira:
echo 1. Buildar o backend em executavel
echo 2. Buildar o frontend para producao
echo 3. Criar pacote de distribuicao
echo.
pause

set BACKEND_DIR=backend
set FRONTEND_DIR=frontend
set DIST_DIR=distribuicao

REM Criar pasta de distribuicao
if exist %DIST_DIR% (
    echo Limpando pasta de distribuicao anterior...
    rmdir /s /q %DIST_DIR%
)
mkdir %DIST_DIR%

echo.
echo ========================================
echo [1/3] Build do Backend
echo ========================================
echo.
cd %BACKEND_DIR%
call build_windows.bat
if errorlevel 1 (
    echo ERRO no build do backend!
    pause
    exit /b 1
)
cd ..

REM Copiar backend para distribuicao
if exist %BACKEND_DIR%\dist\financas-backend\financas-backend.exe (
    echo Copiando executavel do backend (pasta completa)...
    xcopy /E /I /Y %BACKEND_DIR%\dist\financas-backend %DIST_DIR%\financas-backend
    echo Renomeando executavel para nome mais simples...
    copy %DIST_DIR%\financas-backend\financas-backend.exe %DIST_DIR%\financas-backend.exe
    if exist %BACKEND_DIR%\dist\financas-backend\.env.example (
        copy %BACKEND_DIR%\dist\financas-backend\.env.example %DIST_DIR%\.env.example
    ) else if exist %BACKEND_DIR%\.env.example (
        copy %BACKEND_DIR%\.env.example %DIST_DIR%\.env.example
    )
) else if exist %BACKEND_DIR%\dist\financas-backend.exe (
    echo Copiando executavel do backend...
    copy %BACKEND_DIR%\dist\financas-backend.exe %DIST_DIR%\
    if exist %BACKEND_DIR%\dist\.env.example (
        copy %BACKEND_DIR%\dist\.env.example %DIST_DIR%\.env.example
    ) else if exist %BACKEND_DIR%\.env.example (
        copy %BACKEND_DIR%\.env.example %DIST_DIR%\.env.example
    )
) else (
    echo AVISO: Executavel do backend nao encontrado!
)

echo.
echo ========================================
echo [2/3] Build do Frontend
echo ========================================
echo.
cd %FRONTEND_DIR%

REM Verificar Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Node.js nao encontrado!
    echo Instale Node.js antes de continuar.
    pause
    exit /b 1
)

REM Instalar dependencias
echo Instalando dependencias do frontend...
call npm install
if errorlevel 1 (
    echo ERRO ao instalar dependencias do frontend!
    pause
    exit /b 1
)

REM Build de producao
echo.
echo Gerando build de producao do frontend...
call npm run build
if errorlevel 1 (
    echo ERRO no build do frontend!
    pause
    exit /b 1
)

cd ..

REM Copiar frontend para distribuicao
if exist %FRONTEND_DIR%\out (
    echo Copiando build do frontend...
    xcopy /E /I /Y %FRONTEND_DIR%\out %DIST_DIR%\frontend
) else if exist %FRONTEND_DIR%\.next (
    echo Copiando build do frontend (Next.js)...
    xcopy /E /I /Y %FRONTEND_DIR%\.next %DIST_DIR%\frontend\.next
    xcopy /E /I /Y %FRONTEND_DIR%\public %DIST_DIR%\frontend\public
    copy %FRONTEND_DIR%\package.json %DIST_DIR%\frontend\
    copy %FRONTEND_DIR%\next.config.js %DIST_DIR%\frontend\ 2>nul
    copy %FRONTEND_DIR%\next.config.ts %DIST_DIR%\frontend\ 2>nul
) else (
    echo AVISO: Build do frontend nao encontrado!
)

echo.
echo ========================================
echo [3/3] Criando Launcher e Documentacao
echo ========================================
echo.

REM Criar launcher principal
echo Criando launcher principal...
(
echo @echo off
echo echo ========================================
echo echo  Financas Pessoais - Sistema Completo
echo echo ========================================
echo echo.
echo cd /d "%%~dp0"
echo.
echo echo Verificando executavel do backend...
echo if exist financas-backend\financas-backend.exe ^(
echo     set BACKEND_EXE=financas-backend\financas-backend.exe
echo ^) else if exist financas-backend.exe ^(
echo     set BACKEND_EXE=financas-backend.exe
echo ^) else ^(
echo     echo ERRO: Executavel do backend nao encontrado!
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo Iniciando backend...
echo start "Backend - Financas Pessoais" /MIN "%%BACKEND_EXE%%"
echo.
echo echo Aguardando backend iniciar...
echo timeout /t 5 /nobreak ^>nul
echo.
echo echo Abrindo frontend no navegador...
echo start http://localhost:3000
echo.
echo echo Sistema iniciado!
echo echo - Backend: http://localhost:8000/docs
echo echo - Frontend: http://localhost:3000
echo echo.
echo echo Pressione qualquer tecla para encerrar o backend...
echo pause ^>nul
echo taskkill /F /FI "WindowTitle eq Backend - Financas Pessoais*" 2^>nul
echo echo.
echo echo Sistema encerrado.
) > %DIST_DIR%\Iniciar_Financas_Pessoais.bat

REM Criar README de distribuicao
echo Criando documentacao de distribuicao...
(
echo # Financas Pessoais - Guia de Instalacao
echo.
echo ## Requisitos do Sistema
echo.
echo - Windows 10/11 64-bit
echo - PostgreSQL 15+ instalado e configurado
echo - Conexao com internet ^(para download de dependencias^)
echo.
echo ## Instalacao
echo.
echo 1. Extraia todos os arquivos para uma pasta
echo 2. Configure o arquivo `.env` com suas credenciais do PostgreSQL
echo 3. Certifique-se de que o PostgreSQL esta rodando
echo 4. Execute `Iniciar_Financas_Pessoais.bat`
echo.
echo ## Configuracao do .env
echo.
echo Copie o arquivo `.env.example` para `.env` e configure:
echo.
echo - `DATABASE_URL`: URL de conexao com PostgreSQL
echo - `SECRET_KEY`: Chave secreta para JWT
echo.
echo ## Suporte
echo.
echo Para mais informacoes, consulte a documentacao completa.
) > %DIST_DIR%\LEIA-ME.txt

echo.
echo ========================================
echo  Build Completo Finalizado!
echo ========================================
echo.
echo Pacote de distribuicao criado em: %DIST_DIR%
echo.
echo Conteudo:
echo - financas-backend.exe ^(Backend^)
echo - frontend/ ^(Frontend buildado^)
echo - Iniciar_Financas_Pessoais.bat ^(Launcher^)
echo - LEIA-ME.txt ^(Documentacao^)
echo.
echo Pronto para distribuicao!
echo.
pause

