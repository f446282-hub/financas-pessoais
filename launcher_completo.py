"""
Launcher completo do sistema Finanças Pessoais
Inicia backend e frontend automaticamente
"""

import os
import sys
import subprocess
import time
import webbrowser
import shutil
from pathlib import Path

def main():
    print("=" * 60)
    print("  💰 Finanças Pessoais - Iniciando Sistema")
    print("=" * 60)
    print()
    
    # Caminhos
    base_dir = Path(__file__).parent
    backend_dir = base_dir / "backend"
    frontend_dir = base_dir / "frontend"
    
    # Verificar diretórios
    if not backend_dir.exists():
        print("❌ ERRO: Pasta 'backend' não encontrada!")
        input("\nPressione Enter para sair...")
        sys.exit(1)
    
    if not frontend_dir.exists():
        print("❌ ERRO: Pasta 'frontend' não encontrada!")
        input("\nPressione Enter para sair...")
        sys.exit(1)
    
    processes = []
    
    try:
        # 1. Verificar e configurar backend para SQLite
        print("[1/4] Verificando configuração do backend...")
        backend_env = backend_dir / ".env"
        
        if not backend_env.exists():
            print("   Configurando SQLite automaticamente...")
            sqlite_config = """DATABASE_URL=sqlite:///./financas_pessoais.db
SECRET_KEY=local-development-key-change-in-production-12345
DEBUG=true
ENVIRONMENT=development
CORS_ORIGINS=["http://localhost:3000"]
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
"""
            backend_env.write_text(sqlite_config, encoding='utf-8')
            print("   ✓ Configuração SQLite criada!")
        
        # Verificar se precisa executar migrations
        db_file = backend_dir / "financas_pessoais.db"
        if not db_file.exists():
            print("   Banco SQLite não encontrado. Executando migrations...")
            venv_python = backend_dir / "venv" / "Scripts" / "python.exe"
            
            if venv_python.exists():
                try:
                    subprocess.run(
                        [str(venv_python), "-m", "alembic", "upgrade", "head"],
                        cwd=str(backend_dir),
                        check=True,
                        capture_output=True
                    )
                    print("   ✓ Migrations executadas!")
                except subprocess.CalledProcessError:
                    print("   ⚠ Aviso: Não foi possível executar migrations automaticamente.")
                    print("   Execute manualmente depois se necessário.")
        
        # 2. Iniciar Backend
        print("\n[2/4] Iniciando Backend...")
        venv_python = backend_dir / "venv" / "Scripts" / "python.exe"
        venv_activate = backend_dir / "venv" / "Scripts" / "activate.bat"
        
        if venv_python.exists():
            backend_cmd = [str(venv_python), "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"]
        else:
            backend_cmd = ["python", "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"]
        
        # Criar janela separada para backend
        if sys.platform == "win32":
            backend_process = subprocess.Popen(
                backend_cmd,
                cwd=str(backend_dir),
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            backend_process = subprocess.Popen(
                backend_cmd,
                cwd=str(backend_dir)
            )
        
        processes.append(backend_process)
        print(f"   ✓ Backend iniciado (PID: {backend_process.pid})")
        print("   📍 http://localhost:8000")
        
        # Aguardar backend iniciar
        print("\n   Aguardando backend iniciar...")
        time.sleep(5)
        
        # 3. Verificar Frontend
        print("\n[3/4] Verificando Frontend...")
        node_modules = frontend_dir / "node_modules"
        
        if not node_modules.exists():
            print("   ⚠ Dependências do frontend não encontradas!")
            print("   Execute primeiro: cd frontend && npm install")
            print("\n   Continuando mesmo assim...")
        
        # 4. Iniciar Frontend
        print("\n[4/4] Iniciando Frontend...")
        
        # Encontrar npm no PATH
        npm_path = shutil.which("npm")
        if not npm_path:
            print("   ⚠ npm não encontrado no PATH!")
            print("   Tentando caminhos comuns...")
            
            # Tentar caminhos comuns do Node.js no Windows
            common_paths = [
                r"C:\Program Files\nodejs\npm.cmd",
                r"C:\Program Files (x86)\nodejs\npm.cmd",
                os.path.expanduser(r"~\AppData\Roaming\npm\npm.cmd"),
            ]
            
            npm_path = None
            for path in common_paths:
                if os.path.exists(path):
                    npm_path = path
                    break
            
            if not npm_path:
                print("   ❌ ERRO: npm não encontrado!")
                print("   Instale Node.js de: https://nodejs.org/")
                raise FileNotFoundError("npm não encontrado no sistema")
        
        print(f"   ✓ npm encontrado: {npm_path}")
        
        # Executar npm
        if sys.platform == "win32":
            frontend_process = subprocess.Popen(
                [npm_path, "run", "dev"],
                cwd=str(frontend_dir),
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                shell=False
            )
        else:
            frontend_process = subprocess.Popen(
                [npm_path, "run", "dev"],
                cwd=str(frontend_dir)
            )
        
        processes.append(frontend_process)
        print(f"   ✓ Frontend iniciado (PID: {frontend_process.pid})")
        print("   📍 http://localhost:3000")
        
        # Aguardar frontend iniciar
        print("\n   Aguardando frontend iniciar...")
        time.sleep(8)
        
        # 5. Abrir navegador
        print("\n" + "=" * 60)
        print("  ✅ Sistema Iniciado com Sucesso!")
        print("=" * 60)
        print("\n📍 Acesse:")
        print("   - Frontend: http://localhost:3000")
        print("   - Backend API: http://localhost:8000/docs")
        print("\n💡 Para encerrar, feche este programa ou as janelas do Backend e Frontend")
        print("\nAbrindo navegador...")
        
        webbrowser.open("http://localhost:3000")
        
        # Manter programa aberto
        print("\n" + "=" * 60)
        print("  Sistema rodando... Pressione ENTER para encerrar")
        print("=" * 60)
        
        # Tentar input, mas se não funcionar (em .exe), apenas aguardar
        try:
            input()
        except (EOFError, RuntimeError):
            # Quando compilado como .exe, input pode não funcionar
            print("\n  (Aguardando indefinidamente - feche esta janela para encerrar)")
            try:
                while True:
                    time.sleep(60)
            except KeyboardInterrupt:
                pass
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Encerrando sistema...")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("\nDetalhes do erro:")
        import traceback
        traceback.print_exc()
        
        # Tentar input, mas se não funcionar, apenas aguardar
        try:
            input("\nPressione Enter para sair...")
        except (EOFError, RuntimeError):
            print("\nPressione qualquer tecla ou feche a janela...")
            time.sleep(10)
    finally:
        # Encerrar processos
        print("\n🛑 Encerrando processos...")
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
        
        print("✅ Sistema encerrado!")
        time.sleep(2)


if __name__ == "__main__":
    main()

