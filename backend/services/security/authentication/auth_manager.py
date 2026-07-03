import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class AuthManager:
    """Handles user authentication, sessions, and workspaces."""
    def __init__(self):
        self.active_sessions: Dict[str, Dict[str, Any]] = {}

    def login(self, username: str, password_hash: str) -> Optional[str]:
        if username == 'admin' and password_hash == 'hash':
            session_id = 'sess_123'
            self.active_sessions[session_id] = {'username': username, 'role': 'admin'}
            return session_id
        return None

    def validate_session(self, session_id: str) -> bool:
        return session_id in self.active_sessions