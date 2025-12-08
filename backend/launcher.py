"""
Launcher para o executável do backend.
Este arquivo será usado pelo PyInstaller para criar o .exe
"""

import os
import sys
import uvicorn
from pathlib import Path

# Ajustar o path para incluir o app
if getattr(sys, 'frozen', False):
    # Se está rodando como executável
    base_path = Path(sys._MEIPASS)
    app_path = base_path / "app"
else:
    # Se está rodando como script
    base_path = Path(__file__).parent
    app_path = base_path / "app"

# Adicionar app ao path
sys.path.insert(0, str(base_path))
sys.path.insert(0, str(app_path.parent))

# Importar app
from app.main import app

def main():
    """Inicia o servidor FastAPI."""
    # Porta e host
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "127.0.0.1")
    
    print("=" * 60)
    print("  💰 Finanças Pessoais - Backend")
    print("=" * 60)
    print(f"\n🚀 Iniciando servidor em http://{host}:{port}")
    print(f"📚 Documentação: http://{host}:{port}/docs")
    print("\nPressione CTRL+C para parar o servidor\n")
    
    # Iniciar uvicorn
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Servidor encerrado pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Erro ao iniciar servidor: {e}")
        input("\nPressione Enter para sair...")
        sys.exit(1)

