"""
Script para criar executável do backend usando PyInstaller.
Execute: python build_executable.py
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def main():
    print("=" * 60)
    print("  Build do Executável - Backend Finanças Pessoais")
    print("=" * 60)
    print()
    
    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller
        print("✓ PyInstaller encontrado")
    except ImportError:
        print("✗ PyInstaller não encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller instalado")
    
    # Diretórios
    base_dir = Path(__file__).parent
    dist_dir = base_dir / "dist"
    build_dir = base_dir / "build"
    
    # Limpar builds anteriores
    if dist_dir.exists():
        print("\nLimpando builds anteriores...")
        shutil.rmtree(dist_dir)
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    print("\nIniciando build do executável...")
    print("(Isso pode demorar alguns minutos)")
    print()
    
    # Comando PyInstaller
    # Usando --onedir ao invés de --onefile para melhor compatibilidade
    cmd = [
        "pyinstaller",
        "--name=financas-backend",
        "--onedir",
        "--console",
        "--add-data=app;app",
        "--add-data=.env.example;.",
        "--hidden-import=uvicorn.lifespan.on",
        "--hidden-import=uvicorn.lifespan.off",
        "--hidden-import=uvicorn.protocols.http.auto",
        "--hidden-import=uvicorn.protocols.websockets.auto",
        "--hidden-import=uvicorn.loops.auto",
        "--hidden-import=uvicorn.loops.uvloop",
        "--hidden-import=uvicorn.loops.asyncio",
        "--hidden-import=multipart",
        "--hidden-import=email_validator",
        "--hidden-import=passlib",
        "--hidden-import=passlib.context",
        "--hidden-import=jose",
        "--hidden-import=alembic",
        "--hidden-import=alembic.config",
        "--hidden-import=sqlalchemy",
        "--hidden-import=psycopg2",
        "--collect-all=uvicorn",
        "--collect-all=fastapi",
        "launcher.py"
    ]
    
    try:
        subprocess.check_call(cmd, cwd=str(base_dir))
        print("\n" + "=" * 60)
        print("  ✓ Build concluído com sucesso!")
        print("=" * 60)
        exe_path = dist_dir / "financas-backend" / "financas-backend.exe"
        print(f"\nExecutável criado em: {exe_path}")
        print("\nPróximos passos:")
        print("1. Copie o arquivo .env para a pasta dist/")
        print("2. Teste o executável: dist\\financas-backend.exe")
        print()
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Erro durante o build: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

