import unittest
import sqlite3
import sys
import os

# Add the project root to the python path so tests can run directly if needed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.database.database_manager import DatabaseManager
from backend.database.transaction import TransactionManager


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db_manager = DatabaseManager(":memory:")

    def tearDown(self):
        self.db_manager.disconnect()

    def test_initialize_and_connect(self):
        self.db_manager.initialize()
        conn = self.db_manager.connect()
        self.assertIsInstance(conn, sqlite3.Connection)

        # Check if a table exists
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='business'"
        )
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "business")

    def test_transaction_commit(self):
        self.db_manager.initialize()
        tx_manager = TransactionManager(self.db_manager.connection_manager)

        with tx_manager.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO config (config_key, config_value, updated_at) VALUES (?, ?, ?)",
                ("theme", "dark", "2026-06-28 00:00:00"),
            )

        # Verify it was committed
        conn = self.db_manager.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT config_value FROM config WHERE config_key='theme'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result["config_value"], "dark")

    def test_transaction_rollback(self):
        self.db_manager.initialize()
        tx_manager = TransactionManager(self.db_manager.connection_manager)

        try:
            with tx_manager.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO config (config_key, config_value, updated_at) VALUES (?, ?, ?)",
                    ("theme", "light", "2026-06-28 00:00:00"),
                )
                raise ValueError("Force rollback")
        except ValueError:
            pass

        # Verify it was rolled back
        conn = self.db_manager.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT config_value FROM config WHERE config_key='theme'")
        result = cursor.fetchone()
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
