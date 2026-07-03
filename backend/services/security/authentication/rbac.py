from enum import Enum
from typing import List

class Role(Enum):
    ADMIN = 'admin'
    USER = 'user'
    VIEWER = 'viewer'

class RBACManager:
    """Role-Based Access Control logic."""
    def __init__(self):
        self.role_permissions = {
            Role.ADMIN: ['read', 'write', 'delete', 'execute'],
            Role.USER:  ['read', 'write', 'execute'],
            Role.VIEWER: ['read']
        }

    def has_permission(self, role: Role, action: str) -> bool:
        return action in self.role_permissions.get(role, [])