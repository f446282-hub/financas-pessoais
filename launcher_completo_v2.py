"""
Launcher completo do sistema Finanças Pessoais - Versão 2
Inicia backend e frontend automaticamente
Versão melhorada para funcionar como executável
"""

import os
import sys
import subprocess
import time
import webbrowser
import shutil
from pathlib import Path

def find_executable(name):
    """Encontra um executável no PATH ou caminhos comuns."""
    # Tentar encontrar no PATH
    path = shutil.which(name)
    if path:
        return path
    
    # Se não encontrou e está no Windows, tentar caminhos comuns
    if sys.platform == "win32":
        common_paths = {
            "npm": [
                r"C:\Program Files\nodejs\npm.cmd",
                r"C:\Program Files (x86)\nodejs\npm.cmd",
                os.path.expanduser(r"~\AppData\Roaming\npm\npm.cmd"),
            ],
            "node": [
                r"C:\Program Files\nodejs\node.exe",
                r"C:\Program Files (x86)\nodejs\node.exe",
            ],
            "python": [
                r"C:\Python311\python.exe",
                r"C:\Python312\python.exe",
                os.path.expanduser(r"~\AppData\Local\Programs\Python\Python311\python.exe"),
                os.path.expanduser(r"~\AppData\Local\Programs\Python\Python312\python.exe"),
            ]
        }
        
        if name in common_paths:
            for path in common_paths[name]:
                if os.path.exists(path):
                    return path
    
    return None

def safe_input(prompt=""):
    """Input seguro que funciona mesmo quando compilado como .exe"""
    try:
        return input(prompt)
    except (EOFError, RuntimeError, OSError):
        # Quando compilado como .exe ou stdin não disponível
        print("\n(Pressione qualquer tecla e feche a janela para encerrar)")
        try:
            import msvcrt
            msvcrt.getch()
        except:
            time.sleep(5)
        return ""

def main():
    try:
        print("=" * 60)
        print("  💰 Finanças Pessoais - Iniciando Sistema")
        print("=" * 60)
        print()
        
        # Caminhos - tentar várias opções
        script_dir = Path(__file__).parent.resolve()
        current_dir = Path.cwd().resolve()
        
        # Tentar encontrar as pastas
        backend_dir = None
        frontend_dir = None
        
        # Opção 1: Relativo ao script
        if (script_dir / "backend").exists():
            backend_dir = script_dir / "backend"
            frontend_dir = script_dir / "frontend"
            base_dir = script_dir
        # Opção 2: Relativo ao diretório atual
        elif (current_dir / "backend").exists():
            backend_dir = current_dir / "backend"
            frontend_dir = current_dir / "frontend"
            base_dir = current_dir
        # Opção 3: Procurar recursivamente (limite 3 níveis)
        else:
            for parent in [script_dir, current_dir]:
                for level in range(3):
                    test_backend = parent.parents[level] if level > 0 else parent
                    if (test_backend / "backend").exists() and (test_backend / "frontend").exists():
                        backend_dir = test_backend / "backend"
                        frontend_dir = test_backend / "frontend"
                        base_dir = test_backend
                        break
                if backend_dir:
                    break
        
        # Se ainda não encontrou, mostrar erro detalhado
        if not backend_dir or not backend_dir.exists():
            print("❌ ERRO: Pasta 'backend' não encontrada!")
            print(f"\nCaminhos testados:")
            print(f"  - Script: {script_dir}")
            print(f"  - Atual: {current_dir}")
            print(f"\nCertifique-se de que:")
            print(f"  1. O executável está na raiz do projeto")
            print(f"  2. As pastas 'backend' e 'frontend' existem")
            print(f"  3. Ou execute o arquivo 'Iniciar_Sistema.bat' ao invés do .exe")
            safe_input("\nPressione Enter para sair...")
            sys.exit(1)
        
        if not frontend_dir or not frontend_dir.exists():
            print("❌ ERRO: Pasta 'frontend' não encontrada!")
            print(f"\nBackend encontrado em: {backend_dir}")
            print(f"Frontend não encontrado em: {frontend_dir}")
            safe_input("\nPressione Enter para sair...")
            sys.exit(1)
        
        print(f"✓ Diretórios encontrados:")
        print(f"  - Base: {base_dir}")
        print(f"  - Backend: {backend_dir}")
        print(f"  - Frontend: {frontend_dir}")
        print()
        
        processes = []
        
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
                        capture_output=True,
                        timeout=60
                    )
                    print("   ✓ Migrations executadas!")
                except Exception as e:
                    print(f"   ⚠ Aviso: {e}")
                    print("   Execute manualmente depois se necessário.")
        
        # 2. Iniciar Backend
        print("\n[2/4] Iniciando Backend...")
        venv_python = backend_dir / "venv" / "Scripts" / "python.exe"
        
        if venv_python.exists():
            backend_cmd = [str(venv_python), "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"]
        else:
            python_path = find_executable("python")
            if not python_path:
                print("   ❌ ERRO: Python não encontrado!")
                raise FileNotFoundError("Python não encontrado no sistema")
            backend_cmd = [python_path, "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"]
        
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
        
        npm_path = find_executable("npm")
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
        
        try:
            webbrowser.open("http://localhost:3000")
        except:
            pass
        
        # Manter programa aberto
        print("\n" + "=" * 60)
        print("  Sistema rodando... Pressione ENTER para encerrar")
        print("=" * 60)
        safe_input()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Encerrando sistema...")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("\nDetalhes do erro:")
        try:
            import traceback
            traceback.print_exc()
        except:
            pass
        
        safe_input("\nPressione Enter para sair...")
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

