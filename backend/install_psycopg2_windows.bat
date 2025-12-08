@echo off
echo ========================================
echo  Instalacao do psycopg2-binary no Windows
echo ========================================
echo.

REM Verificar se o ambiente virtual existe
if not exist venv (
    echo ERRO: Ambiente virtual nao encontrado!
    echo Execute primeiro: python -m venv venv
    pause
    exit /b 1
)

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

echo Atualizando pip, setuptools e wheel...
python -m pip install --upgrade pip setuptools wheel

echo.
echo Tentando instalar psycopg2-binary...
echo Isso pode demorar alguns minutos...
echo.

python -m pip install psycopg2-binary --no-cache-dir

if errorlevel 1 (
    echo.
    echo ========================================
    echo  ERRO: Falha na instalacao!
    echo ========================================
    echo.
    echo SOLUCAO 1 - Instalar Microsoft Visual C++ Build Tools:
    echo.
    echo 1. Baixe e instale o Microsoft Visual C++ Build Tools:
    echo    https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo.
    echo 2. Durante a instalacao, selecione:
    echo    - "Desenvolvimento para Desktop com C++"
    echo    - "Ferramentas de build do MSVC"
    echo.
    echo 3. Apos instalar, execute este script novamente.
    echo.
    echo ========================================
    echo SOLUCAO 2 - Usar versao pre-compilada:
    echo ========================================
    echo.
    echo Tente instalar usando uma versao especifica:
    echo   python -m pip install psycopg2-binary==2.9.9
    echo.
    echo ========================================
    echo SOLUCAO 3 - Instalar via wheel:
    echo ========================================
    echo.
    echo Baixe o wheel manualmente de:
    echo https://pypi.org/project/psycopg2-binary/#files
    echo.
    echo Depois instale com:
    echo   python -m pip install nome_do_arquivo.whl
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  SUCESSO! psycopg2-binary instalado!
echo ========================================
echo.
pause

