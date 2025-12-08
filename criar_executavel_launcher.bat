@echo off
echo ========================================
echo  Criar Executavel do Launcher
echo ========================================
echo.
echo Este script cria um executavel .exe que
echo inicia backend e frontend automaticamente.
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    pause
    exit /b 1
)

echo [1/3] Instalando PyInstaller (se necessario)...
echo (Isso pode demorar 1-2 minutos...)
python -m pip install pyinstaller
if errorlevel 1 (
    echo.
    echo ERRO: Falha ao instalar PyInstaller!
    echo.
    echo SOLUCAO: Use o arquivo Iniciar_Sistema.bat que ja funciona!
    echo Ou instale manualmente: python -m pip install pyinstaller
    pause
    exit /b 1
)
echo.
echo ✓ PyInstaller instalado!
echo.

echo.
echo [2/3] Criando executavel...
echo (Isso pode demorar 2-5 minutos - seja paciente!)
echo (Você verá mensagens do PyInstaller, isso é normal)
echo.

echo Usando versao melhorada do launcher (v2)...
python -m PyInstaller ^
    --name="Iniciar_Financas_Pessoais" ^
    --onefile ^
    --console ^
    --icon=NONE ^
    --hidden-import=subprocess ^
    --hidden-import=webbrowser ^
    --hidden-import=shutil ^
    --hidden-import=msvcrt ^
    launcher_completo_v2.py

if errorlevel 1 (
    echo.
    echo ERRO: Falha ao criar executavel!
    pause
    exit /b 1
)

echo.
echo [3/3] Movendo executavel para raiz...
if exist dist\Iniciar_Financas_Pessoais.exe (
    move /Y dist\Iniciar_Financas_Pessoais.exe Iniciar_Financas_Pessoais.exe
    echo.
    echo ========================================
    echo  SUCESSO! Executavel criado!
    echo ========================================
    echo.
    echo Arquivo criado: Iniciar_Financas_Pessoais.exe
    echo.
    echo Agora voce pode:
    echo 1. Duplicar clicando no arquivo para iniciar o sistema
    echo 2. Criar um atalho na area de trabalho
    echo 3. Fixar na barra de tarefas
    echo.
) else (
    echo AVISO: Executavel nao encontrado na pasta dist/
)

echo.
pause

