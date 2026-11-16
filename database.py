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
