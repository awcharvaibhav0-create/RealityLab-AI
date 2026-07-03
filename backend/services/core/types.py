from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict, TypeVar

if TYPE_CHECKING:
    from .events import Event

# Generic payload type
PayloadType = Dict[str, Any]

# Generic return type for agent execution
ReturnType = TypeVar("ReturnType")

# Event callback type
EventCallback = Callable[["Event"], Awaitable[None]]

Context = Dict[str, Any]
