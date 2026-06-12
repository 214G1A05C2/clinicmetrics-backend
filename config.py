import os
from pathlib import Path


class Config:
    _base_dir = Path(__file__).resolve().parent
    _sqlite_db = _base_dir / "instance" / "calls.db"
    _sqlite_uri = _sqlite_db.as_posix()
    _database_url = os.getenv("DATABASE_URL", "").strip() or os.getenv(
        "DATA_BASE_URL", ""
    ).strip()

    # Prefer the bundled SQLite snapshot so the dashboard always has data.
    # If the snapshot is unavailable, fall back to an explicit database URL.
    if _sqlite_db.exists():
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{_sqlite_uri}"
    elif _database_url:
        if _database_url.startswith("postgres://"):
            _database_url = _database_url.replace(
                "postgres://", "postgresql://", 1
            )
        SQLALCHEMY_DATABASE_URI = _database_url
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{_sqlite_uri}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
