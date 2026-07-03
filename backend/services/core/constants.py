from enum import Enum


class AgentState(str, Enum):
    INITIALIZED = "INITIALIZED"
    RUNNING = "RUNNING"
    IDLE = "IDLE"
    ERROR = "ERROR"
    STOPPED = "STOPPED"


class EventPriority(int, Enum):
    LOW = 10
    NORMAL = 20
    HIGH = 30
    CRITICAL = 40


DEFAULT_TIMEOUT = 30.0
MAX_RETRIES = 3
