@echo off
echo ========================================
echo  Criar Atalho na Area de Trabalho
echo ========================================
echo.

set SCRIPT_DIR=%~dp0
set BAT_FILE=%SCRIPT_DIR%Iniciar_Sistema.bat

echo Criando atalho na area de trabalho...
echo.

cscript //nologo criar_atalho_area_trabalho.vbs "%SCRIPT_DIR%"

if errorlevel 1 (
    echo.
    echo Criando atalho manualmente...
    
    REM Criar atalho usando PowerShell
    powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Iniciar Financas Pessoais.lnk'); $Shortcut.TargetPath = '%BAT_FILE%'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.Description = 'Inicia o sistema Financas Pessoais'; $Shortcut.Save()"
    
    if errorlevel 1 (
        echo.
        echo AVISO: Nao foi possivel criar atalho automaticamente.
        echo.
        echo CRIE MANUALMENTE:
        echo 1. Clique com botao direito na area de trabalho
        echo 2. Novo ^> Atalho
        echo 3. Coloque o caminho: %BAT_FILE%
        echo 4. Nome: Iniciar Financas Pessoais
    ) else (
        echo.
        echo ✓ Atalho criado na area de trabalho!
    )
) else (
    echo.
    echo ✓ Atalho criado na area de trabalho!
)

echo.
pause

