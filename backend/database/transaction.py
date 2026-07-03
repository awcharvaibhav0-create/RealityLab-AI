from contextlib import contextmanager
from typing import Iterator
import sqlite3
from .connection import ConnectionManager


class TransactionManager:
    """Provides transactional scope for database operations."""

    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        """
        Provides a transactional scope around a series of operations.
        Commits on success, rollbacks on exception.
        """
        conn = self.connection_manager.get_connection()
        try:
            conn.execute("BEGIN TRANSACTION")
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
