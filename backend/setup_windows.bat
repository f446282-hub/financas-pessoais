@echo off
echo ========================================
echo  Instalacao do Backend - Windows
echo ========================================
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado! Instale Python 3.11+ primeiro.
    pause
    exit /b 1
)

echo [1/5] Criando ambiente virtual...
if exist venv (
    echo Ambiente virtual ja existe. Pulando...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERRO: Falha ao criar ambiente virtual!
        pause
        exit /b 1
    )
    echo Ambiente virtual criado com sucesso!
)
echo.

echo [2/5] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRO: Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)
echo Ambiente virtual ativado!
echo.

echo [3/5] Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools wheel
echo.
echo Instalando pydantic com binary wheels (evita problema com Rust)...
python -m pip install --only-binary :all: pydantic pydantic-core pydantic-settings
if errorlevel 1 (
    echo.
    echo AVISO: Problema ao instalar pydantic com binary wheels.
    echo Tentando versao compativel...
    python -m pip install "pydantic>=2.0.0,<2.6.0" "pydantic-settings>=2.0.0,<2.1.0"
    if errorlevel 1 (
        echo.
        echo AVISO: Problema com pydantic. Veja: SOLUCAO_PYDANTIC.md
        echo Continuando com outras dependencias...
    )
)
echo.
echo Instalando psycopg2-binary (pode demorar alguns minutos no Windows)...
python -m pip install psycopg2-binary --no-cache-dir
if errorlevel 1 (
    echo.
    echo AVISO: Falha ao instalar psycopg2-binary.
    echo Execute depois: install_psycopg2_windows.bat
    echo Ou veja: SOLUCAO_PSYCOPG2.md
)
echo.
echo Instalando outras dependencias...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo AVISO: Algumas dependencias podem ter falhado.
    echo Verifique os erros acima.
    echo.
    echo SOLUCOES:
    echo - pydantic: Veja SOLUCAO_PYDANTIC.md
    echo - psycopg2: Veja SOLUCAO_PSYCOPG2.md
    echo - Ou execute: install_dependencies_windows.bat
    echo.
) else (
    echo Dependencias instaladas com sucesso!
)
echo.

REM Verificar se psycopg2-binary foi instalado
python -c "import psycopg2" >nul 2>&1
if errorlevel 1 (
    echo ========================================
    echo  AVISO: psycopg2-binary nao foi instalado!
    echo ========================================
    echo.
    echo Execute: install_psycopg2_windows.bat
    echo Ou veja: SOLUCAO_PSYCOPG2.md
    echo.
)

echo [4/5] Copiando arquivo .env...
if exist .env (
    echo Arquivo .env ja existe. Pulando...
) else (
    if exist .env.example (
        copy .env.example .env
        echo Arquivo .env criado! Lembre-se de configurar DATABASE_URL e SECRET_KEY.
    ) else (
        echo AVISO: Arquivo .env.example nao encontrado!
    )
)
echo.

echo [5/5] Configuracao concluida!
echo.
echo ========================================
echo  PROXIMOS PASSOS:
echo ========================================
echo.
echo 1. Configure o arquivo .env:
echo    notepad .env
echo.
echo 2. Crie o banco de dados PostgreSQL:
echo    - Use pgAdmin para criar o banco "financas_pessoais"
echo    - Ou execute: psql -U postgres -c "CREATE DATABASE financas_pessoais;"
echo.
echo 3. Execute as migrations:
echo    python -m alembic upgrade head
echo.
echo 4. Inicie o servidor:
echo    python -m uvicorn app.main:app --reload --port 8000
echo.
echo ========================================
pause

