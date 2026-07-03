from typing import TypeVar, Generic, List, Optional, Any, Dict
import sqlite3
from abc import ABC, abstractmethod

T = TypeVar("T")


class BaseRepository(Generic[T], ABC):
    """Abstract base class for data repositories."""

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    @abstractmethod
    def get_table_name(self) -> str:
        """Returns the name of the database table."""
        pass

    @abstractmethod
    def _map_row_to_model(self, row: sqlite3.Row) -> T:
        """Maps a database row to a domain model."""
        pass

    def get_by_id(self, id_value: Any, id_column: str = "id") -> Optional[T]:
        """Retrieves a single record by its ID."""
        cursor = self.connection.cursor()
        query = f"SELECT * FROM {self.get_table_name()} WHERE {id_column} = ?"
        cursor.execute(query, (id_value,))
        row = cursor.fetchone()
        if row:
            return self._map_row_to_model(row)
        return None

    def get_all(self) -> List[T]:
        """Retrieves all records from the table."""
        cursor = self.connection.cursor()
        query = f"SELECT * FROM {self.get_table_name()}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [self._map_row_to_model(row) for row in rows]

    def delete(self, id_value: Any, id_column: str = "id") -> bool:
        """Deletes a record by its ID."""
        cursor = self.connection.cursor()
        query = f"DELETE FROM {self.get_table_name()} WHERE {id_column} = ?"
        cursor.execute(query, (id_value,))
        self.connection.commit()
        return cursor.rowcount > 0

    def insert(self, data: Dict[str, Any]) -> int:
        """Inserts a new record into the table."""
        cursor = self.connection.cursor()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        query = (
            f"INSERT INTO {self.get_table_name()} ({columns}) VALUES ({placeholders})"
        )
        cursor.execute(query, tuple(data.values()))
        self.connection.commit()
        return cursor.lastrowid
