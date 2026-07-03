import sqlite3
from .connection import ConnectionManager
from .schema_manager import SchemaManager


class DatabaseManager:
    """High-level manager for database initialization and access."""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.connection_manager = ConnectionManager(self.db_path)

    def initialize(self):
        """Initializes the database schema."""
        conn = self.connect()
        schema_manager = SchemaManager(conn)
        schema_manager.create_tables()

    def connect(self) -> sqlite3.Connection:
        """Gets a database connection."""
        return self.connection_manager.get_connection()

    def disconnect(self):
        """Closes the current database connection."""
        self.connection_manager.close_connection()

    def begin_transaction(self):
        """Begins a transaction on the current connection."""
        self.connect().execute("BEGIN TRANSACTION")

    def commit(self):
        """Commits the current transaction."""
        self.connect().commit()

    def rollback(self):
        """Rolls back the current transaction."""
        self.connect().rollback()
