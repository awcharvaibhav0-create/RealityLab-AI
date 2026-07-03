import unittest
import sqlite3
import sys
import os

# Add the project root to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.database.database_manager import DatabaseManager
from backend.database.repository import BaseRepository
from backend.database.models import Config


class SystemConfigRepository(BaseRepository[Config]):
    def get_table_name(self) -> str:
        return "config"

    def _map_row_to_model(self, row: sqlite3.Row) -> Config:
        return Config(
            config_key=row["config_key"],
            config_value=row["config_value"],
            updated_at=row["updated_at"],
        )


class TestRepository(unittest.TestCase):
    def setUp(self):
        self.db_manager = DatabaseManager(":memory:")
        self.db_manager.initialize()
        self.conn = self.db_manager.connect()
        self.repo = SystemConfigRepository(self.conn)

    def tearDown(self):
        self.db_manager.disconnect()

    def test_insert_and_get_by_id(self):
        data = {
            "config_key": "version",
            "config_value": "1.0.0",
            "updated_at": "2026-06-28 00:00:00",
        }
        self.repo.insert(data)

        result = self.repo.get_by_id("version", "config_key")
        self.assertIsNotNone(result)
        self.assertEqual(result.config_key, "version")
        self.assertEqual(result.config_value, "1.0.0")

    def test_get_all(self):
        self.repo.insert(
            {
                "config_key": "k1",
                "config_value": "v1",
                "updated_at": "2026-06-28 00:00:00",
            }
        )
        self.repo.insert(
            {
                "config_key": "k2",
                "config_value": "v2",
                "updated_at": "2026-06-28 00:00:00",
            }
        )

        results = self.repo.get_all()
        self.assertEqual(len(results), 2)
        keys = {r.config_key for r in results}
        self.assertEqual(keys, {"k1", "k2"})

    def test_delete(self):
        self.repo.insert(
            {
                "config_key": "k1",
                "config_value": "v1",
                "updated_at": "2026-06-28 00:00:00",
            }
        )

        deleted = self.repo.delete("k1", "config_key")
        self.assertTrue(deleted)

        result = self.repo.get_by_id("k1", "config_key")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
