@echo off
echo ========================================
echo  Verificacao de Requisitos do Sistema
echo ========================================
echo.

set ALL_OK=1

REM Verificar Python
echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo    ✗ Python NAO encontrado!
    echo    Instale Python 3.11+ de: https://www.python.org/
    set ALL_OK=0
) else (
    python --version
    echo    ✓ Python encontrado!
)

REM Verificar Node.js
echo.
echo [2/4] Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo    ✗ Node.js NAO encontrado!
    echo    Instale Node.js 18+ de: https://nodejs.org/
    set ALL_OK=0
) else (
    node --version
    echo    ✓ Node.js encontrado!
)

REM Verificar npm
echo.
echo [3/4] Verificando npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo    ✗ npm NAO encontrado!
    echo    (Geralmente vem com Node.js)
    set ALL_OK=0
) else (
    npm --version
    echo    ✓ npm encontrado!
)

REM Verificar estrutura do projeto
echo.
echo [4/4] Verificando estrutura do projeto...
cd /d "%~dp0"

if not exist backend (
    echo    ✗ Pasta backend NAO encontrada!
    set ALL_OK=0
) else (
    echo    ✓ Pasta backend encontrada!
)

if not exist frontend (
    echo    ✗ Pasta frontend NAO encontrada!
    set ALL_OK=0
) else (
    echo    ✓ Pasta frontend encontrada!
)

echo.
echo ========================================
if %ALL_OK%==1 (
    echo  ✓ TODOS OS REQUISITOS ATENDIDOS!
    echo ========================================
    echo.
    echo Voce pode executar: Iniciar_Sistema.bat
) else (
    echo  ⚠ ALGUNS REQUISITOS FALTANDO
    echo ========================================
    echo.
    echo Instale os itens faltantes acima antes de continuar.
)
echo.
pause

