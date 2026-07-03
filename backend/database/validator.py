import sqlite3
import os


class DatabaseValidator:
    """Validates the integrity of the database."""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def check_integrity(self) -> bool:
        """Runs PRAGMA integrity_check."""
        if not os.path.exists(self.db_path):
            return False

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check;")
            result = cursor.fetchone()
            conn.close()
            return result and result[0] == "ok"
        except sqlite3.Error:
            return False

    def check_foreign_keys(self) -> bool:
        """Runs PRAGMA foreign_key_check."""
        if not os.path.exists(self.db_path):
            return False

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_key_check;")
            results = cursor.fetchall()
            conn.close()
            return len(results) == 0
        except sqlite3.Error:
            return False
