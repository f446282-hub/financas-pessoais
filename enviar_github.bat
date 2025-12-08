@echo off
echo ========================================
echo  Enviar Projeto para GitHub
echo ========================================
echo.

REM Verificar Git
git --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Git nao encontrado!
    echo.
    echo Instale Git de: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo Git encontrado!
git --version
echo.

REM Ir para raiz do projeto
cd /d "%~dp0"

echo ========================================
echo  Configuracao Inicial
echo ========================================
echo.

REM Verificar se git esta configurado
git config --global user.name >nul 2>&1
if errorlevel 1 (
    echo Git nao esta configurado. Vamos configurar agora.
    echo.
    set /p GIT_NAME="Digite seu nome: "
    set /p GIT_EMAIL="Digite seu email: "
    git config --global user.name "%GIT_NAME%"
    git config --global user.email "%GIT_EMAIL%"
    echo.
    echo ✓ Git configurado!
) else (
    echo Git ja esta configurado:
    git config --global user.name
    git config --global user.email
)

echo.
echo ========================================
echo  Preparando Repositorio
echo ========================================
echo.

REM Verificar se ja e um repositorio git
if not exist .git (
    echo Inicializando repositorio Git...
    git init
    echo ✓ Repositorio inicializado!
) else (
    echo ✓ Repositorio Git ja existe!
)

echo.
echo ========================================
echo  Adicionando Arquivos
echo ========================================
echo.

echo Adicionando arquivos ao Git...
git add .
if errorlevel 1 (
    echo ERRO ao adicionar arquivos!
    pause
    exit /b 1
)

echo ✓ Arquivos adicionados!
echo.

REM Verificar se ja tem commits
git log --oneline -1 >nul 2>&1
if errorlevel 1 (
    echo ========================================
    echo  Primeiro Commit
    echo ========================================
    echo.
    set /p COMMIT_MSG="Digite a mensagem do commit (ou pressione Enter para padrao): "
    if "%COMMIT_MSG%"=="" (
        set COMMIT_MSG=Primeiro commit: Sistema Financas Pessoais
    )
    git commit -m "%COMMIT_MSG%"
    if errorlevel 1 (
        echo.
        echo AVISO: Nenhum arquivo novo para commitar.
        echo (Talvez tudo ja esteja commitado)
    ) else (
        echo.
        echo ✓ Primeiro commit realizado!
    )
) else (
    echo ========================================
    echo  Novo Commit
    echo ========================================
    echo.
    set /p COMMIT_MSG="Digite a mensagem do commit: "
    git commit -m "%COMMIT_MSG%"
    if errorlevel 1 (
        echo.
        echo AVISO: Nenhuma mudanca para commitar.
    ) else (
        echo.
        echo ✓ Commit realizado!
    )
)

echo.
echo ========================================
echo  Conectar com GitHub
echo ========================================
echo.

REM Verificar se ja tem remote
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo Para conectar com GitHub, preciso do URL do seu repositorio.
    echo.
    echo Exemplo: https://github.com/SEU_USUARIO/financas-pessoais.git
    echo.
    set /p GITHUB_URL="Cole o URL do repositorio GitHub: "
    
    if "%GITHUB_URL%"=="" (
        echo.
        echo URL nao fornecido. Pulando conexao...
        echo.
        echo Para conectar depois, execute:
        echo   git remote add origin URL_DO_REPOSITORIO
    ) else (
        git remote add origin "%GITHUB_URL%"
        echo.
        echo ✓ Conectado com GitHub!
    )
) else (
    echo ✓ Ja conectado com GitHub:
    git remote get-url origin
)

echo.
echo ========================================
echo  Enviar para GitHub
echo ========================================
echo.

REM Verificar branch
git branch --show-current >nul 2>&1
if errorlevel 1 (
    echo Criando branch main...
    git branch -M main
)

echo Deseja enviar para o GitHub agora?
choice /C SN /M "Enviar (push) para GitHub"
if errorlevel 2 (
    echo.
    echo OK. Para enviar depois, execute:
    echo   git push -u origin main
    pause
    exit /b 0
)

echo.
echo Enviando para GitHub...
echo (Se pedir login, use seu usuario e Personal Access Token como senha)
echo.

git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo  ERRO ao enviar!
    echo ========================================
    echo.
    echo Possiveis causas:
    echo 1. Nao esta logado no GitHub
    echo 2. Repositorio nao existe no GitHub
    echo 3. URL incorreto
    echo.
    echo SOLUCOES:
    echo - Crie o repositorio no GitHub primeiro
    echo - Use Personal Access Token como senha
    echo - Ou use GitHub Desktop (mais facil)
    echo.
) else (
    echo.
    echo ========================================
    echo  SUCESSO!
    echo ========================================
    echo.
    echo Projeto enviado para GitHub!
    echo.
    git remote get-url origin
)

echo.
pause

