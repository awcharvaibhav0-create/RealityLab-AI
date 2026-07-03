import sqlite3
import threading


class ConnectionManager:
    """Manages SQLite database connections per thread."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.local = threading.local()

    def get_connection(self) -> sqlite3.Connection:
        """Retrieves or creates a connection for the current thread."""
        if getattr(self.local, "connection", None) is None:
            self.local.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                isolation_level=None, # Disable implicit transactions for immediate read consistency
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            )
            # Use dictionary-like row factory for easier mapping
            self.local.connection.row_factory = sqlite3.Row
            # Enable foreign keys
            self.local.connection.execute("PRAGMA foreign_keys = 1")
        return self.local.connection

    def close_connection(self):
        """Closes the connection for the current thread."""
        if getattr(self.local, "connection", None) is not None:
            self.local.connection.close()
            self.local.connection = None
