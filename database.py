import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).with_name("miaiurl.db")


def init_db() -> None:
    with closing(sqlite3.connect(DB_PATH)) as connection:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS links (
                    code TEXT PRIMARY KEY NOT NULL,
                    target_url TEXT NOT NULL,
                    clicks INTEGER NOT NULL DEFAULT 0 CHECK (clicks >= 0)
                )
            """)


def create_link(target_url: str) -> str:
    from secrets import token_urlsafe

    with closing(sqlite3.connect(DB_PATH)) as connection:
        with connection:
            while True:
                code = token_urlsafe(6)
                result = connection.execute(
                    "INSERT INTO links (code, target_url) VALUES (?, ?) "
                    "ON CONFLICT(code) DO NOTHING",
                    (code, target_url),
                )
                if result.rowcount == 1:
                    return code

                    
def resolve_link(code: str) -> str | None:
    with closing(sqlite3.connect(DB_PATH)) as connection:
        with connection:
            row = connection.execute(
                "UPDATE links SET clicks = clicks + 1 "
                "WHERE code = ? RETURNING target_url",
                (code,),
            ).fetchone()
    return row[0] if row is not None else None

