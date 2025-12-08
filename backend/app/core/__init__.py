"""
Core module - Configurações e utilitários centrais.
"""

from app.core.config import settings
from app.core.database import Base, get_db, engine, SessionLocal
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token,
)
from app.core.dependencies import (
    get_current_user,
    get_current_active_user,
    CurrentUser,
    DatabaseSession,
)

__all__ = [
    "settings",
    "Base",
    "get_db",
    "engine",
    "SessionLocal",
    "verify_password",
    "get_password_hash",
    "create_access_token",
    "decode_access_token",
    "get_current_user",
    "get_current_active_user",
    "CurrentUser",
    "DatabaseSession",
]
