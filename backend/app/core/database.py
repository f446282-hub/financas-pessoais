"""
Configuração do banco de dados PostgreSQL.
Define engine, sessão e base para models.
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from app.core.config import settings


# Engine do SQLAlchemy
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Verifica conexão antes de usar
    pool_size=10,
    max_overflow=20,
    echo=settings.debug,  # Log SQL em debug mode
)

# Fábrica de sessões
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base para os models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency que fornece uma sessão do banco de dados.
    Garante que a sessão é fechada após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
