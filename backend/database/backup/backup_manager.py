import os
import shutil
import datetime


class BackupManager:
    """Handles SQLite database backups and restores."""

    def __init__(self, db_path: str, backup_dir: str):
        self.db_path = db_path
        self.backup_dir = backup_dir
        os.makedirs(self.backup_dir, exist_ok=True)

    def create_backup(self) -> str:
        """Creates a backup of the current database file."""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database file not found: {self.db_path}")

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}.sqlite"
        backup_path = os.path.join(self.backup_dir, backup_name)

        shutil.copy2(self.db_path, backup_path)
        return backup_path

    def restore_backup(self, backup_path: str) -> bool:
        """Restores the database from a backup file."""
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup file not found: {backup_path}")

        # Optional: verify backup integrity before replacing
        shutil.copy2(backup_path, self.db_path)
        return True
