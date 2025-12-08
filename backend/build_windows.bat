@echo off
echo ========================================
echo  Build Executavel - Backend Windows
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    pause
    exit /b 1
)

REM Ativar ambiente virtual se existir
if exist venv\Scripts\activate.bat (
    echo Ativando ambiente virtual...
    call venv\Scripts\activate.bat
)

REM Instalar dependencias de build
echo [1/3] Instalando dependencias de build...
python -m pip install -r requirements-build.txt
if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias!
    pause
    exit /b 1
)

REM Executar build
echo.
echo [2/3] Gerando executavel...
echo (Isso pode demorar alguns minutos)
echo.
python build_executable.py
if errorlevel 1 (
    echo ERRO: Falha no build!
    pause
    exit /b 1
)

echo.
echo [3/3] Verificando resultado...
if exist dist\financas-backend\financas-backend.exe (
    echo Executavel encontrado: dist\financas-backend\financas-backend.exe
    if exist .env.example (
        copy .env.example dist\financas-backend\.env.example
    )
) else if exist dist\financas-backend.exe (
    echo Executavel encontrado: dist\financas-backend.exe
    if exist .env.example (
        copy .env.example dist\.env.example
    )
) else (
    echo AVISO: Executavel nao encontrado na pasta dist/
)

echo.
echo ========================================
echo  Build Concluido!
echo ========================================
echo.
echo Executavel criado em: dist\
echo.
echo IMPORTANTE:
echo 1. Configure o arquivo .env na pasta dist/
echo 2. Certifique-se de que o PostgreSQL esta configurado
echo 3. Teste o executavel antes de distribuir
echo.
pause

