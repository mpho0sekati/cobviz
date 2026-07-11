from enum import Enum
from typing import List, Set

class Role(Enum):
    VIEWER = "viewer"
    ANALYST = "analyst"
    ADMIN = "admin"

class Permission(Enum):
    VIEW_DIAGRAM = "view_diagram"
    RUN_AI = "run_ai"
    MANAGE_KEYS = "manage_keys"
    VIEW_AUDIT = "view_audit"

ROLE_PERMISSIONS = {
    Role.VIEWER: {Permission.VIEW_DIAGRAM},
    Role.ANALYST: {Permission.VIEW_DIAGRAM, Permission.RUN_AI},
    Role.ADMIN: {Permission.VIEW_DIAGRAM, Permission.RUN_AI, Permission.MANAGE_KEYS, Permission.VIEW_AUDIT}
}

def has_permission(role_name: str, permission: Permission) -> bool:
    try:
        role = Role(role_name.lower())
        return permission in ROLE_PERMISSIONS.get(role, set())
    except ValueError:
        return False
