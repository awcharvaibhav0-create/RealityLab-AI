from datetime import datetime


class AuditLogger:
    """Logs security events and system actions."""

    def __init__(self, db_manager):
        """Initializes with a DatabaseManager instance."""
        self.db_manager = db_manager

    def log_event(self, action: str, user_id: str, details: str):
        """Records an audit event to the database."""
        timestamp = datetime.now()

        # Generate a simple unique ID for the audit log entry
        log_id = f"audit_{timestamp.strftime('%Y%m%d%H%M%S%f')}"

        query = """
            INSERT INTO audit_logs (id, action, user_id, details, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """
        try:
            self.db_manager.connect().execute(
                query, (log_id, action, user_id, details, timestamp)
            )
            self.db_manager.commit()
        except Exception as e:
            # Fallback to standard logging if DB fails, to ensure audit trail is preserved
            import logging

            logging.getLogger("audit").error(
                f"Failed to write audit log to DB: {e}. Event: {action} by {user_id}: {details}"
            )
