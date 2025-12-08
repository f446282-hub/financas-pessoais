@echo off
echo ========================================
echo  Instalacao de Dependencias - Windows
echo ========================================
echo.
echo Este script instala todas as dependencias
echo resolvendo problemas comuns do Windows.
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    pause
    exit /b 1
)

REM Verificar ambiente virtual
if not exist venv (
    echo ERRO: Ambiente virtual nao encontrado!
    echo Execute primeiro: python -m venv venv
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

echo.
echo [1/5] Atualizando pip, setuptools e wheel...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo AVISO: Problema ao atualizar pip, continuando...
)

echo.
echo [2/5] Instalando pydantic com binary wheels...
echo (Pode aparecer erro sobre Rust, mas e normal - sera resolvido automaticamente)
python -m pip install --only-binary :all: pydantic pydantic-core pydantic-settings 2>nul
if errorlevel 1 (
    echo.
    echo Instalando pydantic (pode aparecer aviso sobre Rust, ignore)...
    python -m pip install pydantic pydantic-core pydantic-settings
    if errorlevel 1 (
        echo.
        echo Tentando versao compativel de pydantic...
        python -m pip install "pydantic>=2.0.0,<2.6.0" "pydantic-settings>=2.0.0,<2.1.0"
    )
)

echo.
echo [3/5] Instalando psycopg2-binary...
python -m pip install psycopg2-binary --no-cache-dir
if errorlevel 1 (
    echo.
    echo AVISO: Problema ao instalar psycopg2-binary.
    echo Execute depois: install_psycopg2_windows.bat
)

echo.
echo [4/5] Instalando outras dependencias (ignorando pydantic ja instalado)...
python -m pip install -r requirements.txt --no-deps
python -m pip install fastapi uvicorn sqlalchemy alembic python-jose passlib bcrypt python-dotenv httpx pytest pytest-asyncio python-multipart email-validator
if errorlevel 1 (
    echo.
    echo Tentando instalar todas as dependencias novamente...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo AVISO: Algumas dependencias podem ter falhado.
        echo Mas vamos verificar o que realmente esta instalado...
    )
)

echo.
echo [5/5] Verificando instalacao final...
echo.
set ALL_OK=1

python -c "import pydantic; print('✓ pydantic instalado')" 2>nul
if errorlevel 1 (
    echo ✗ pydantic NAO instalado
    set ALL_OK=0
)

python -c "import psycopg2; print('✓ psycopg2 instalado')" 2>nul
if errorlevel 1 (
    echo ✗ psycopg2 NAO instalado
    set ALL_OK=0
)

python -c "import fastapi; print('✓ fastapi instalado')" 2>nul
if errorlevel 1 (
    echo ✗ fastapi NAO instalado
    set ALL_OK=0
)

python -c "import sqlalchemy; print('✓ sqlalchemy instalado')" 2>nul
if errorlevel 1 (
    echo ✗ sqlalchemy NAO instalado
    set ALL_OK=0
)

echo.
echo ========================================
if %ALL_OK%==1 (
    echo  ✓ Instalacao Concluida com SUCESSO!
    echo ========================================
    echo.
    echo Todas as dependencias principais estao instaladas.
    echo Voce pode continuar com os proximos passos!
) else (
    echo  ⚠ Instalacao Concluida com AVISOS
    echo ========================================
    echo.
    echo Algumas dependencias podem nao estar instaladas.
    echo Veja os erros acima e tente:
    echo.
    echo - SOLUCAO_PYDANTIC.md (para pydantic)
    echo - SOLUCAO_PSYCOPG2.md (para psycopg2)
    echo - SOLUCAO_RAPIDA.md (para solucoes rapidas)
)
echo.
pause

