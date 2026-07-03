import sqlite3
from typing import List, Optional
from ..connection import ConnectionManager


class BaseRepository:
    """Base repository for all database access."""

    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    @property
    def connection(self) -> sqlite3.Connection:
        """Gets a thread-local database connection."""
        return self.connection_manager.get_connection()

    def execute(self, query: str, parameters: tuple = ()) -> sqlite3.Cursor:
        """Executes a query and returns the cursor."""
        cursor = self.connection.cursor()
        cursor.execute(query, parameters)
        return cursor

    def execute_many(self, query: str, parameters_list: List[tuple]) -> sqlite3.Cursor:
        """Executes a query many times."""
        cursor = self.connection.cursor()
        cursor.executemany(query, parameters_list)
        return cursor

    def fetch_one(self, query: str, parameters: tuple = ()) -> Optional[sqlite3.Row]:
        """Fetches a single row."""
        cursor = self.execute(query, parameters)
        return cursor.fetchone()

    def fetch_all(self, query: str, parameters: tuple = ()) -> List[sqlite3.Row]:
        """Fetches all rows."""
        cursor = self.execute(query, parameters)
        return cursor.fetchall()

    def begin_transaction(self):
        """Begins a transaction."""
        self.execute("BEGIN TRANSACTION")

    def commit(self):
        """Commits the current transaction."""
        self.connection.commit()

    def rollback(self):
        """Rolls back the current transaction."""
        self.connection.rollback()
