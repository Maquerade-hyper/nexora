from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class ExecutionEventType(str, Enum):
    """Events emitted during workflow execution."""

    WORKFLOW_STARTED = "workflow.started"
    NODE_READY = "node.ready"
    NODE_STARTED = "node.started"
    NODE_COMPLETED = "node.completed"
    NODE_FAILED = "node.failed"
    WORKFLOW_COMPLETED = "workflow.completed"
    WORKFLOW_FAILED = "workflow.failed"
    WORKFLOW_CANCELLED = "workflow.cancelled"


@dataclass(frozen=True)
class ExecutionEvent:
    """Immutable event produced during workflow execution."""

    event_type: ExecutionEventType
    workflow_id: str
    run_id: str
    node_id: str | None = None
    message: str | None = None


class ExecutionEventSink(Protocol):
    """Destination for execution events."""

    def emit(self, event: ExecutionEvent) -> None:
        """Receive one execution event."""


class InMemoryExecutionEventSink:
    """Stores execution events in memory."""

    def __init__(self) -> None:
        self._events: list[ExecutionEvent] = []

    def emit(self, event: ExecutionEvent) -> None:
        self._events.append(event)

    @property
    def events(self) -> tuple[ExecutionEvent, ...]:
        return tuple(self._events)

    def clear(self) -> None:
        self._events.clear()

    def by_type(
        self,
        event_type: ExecutionEventType,
    ) -> tuple[ExecutionEvent, ...]:
        return tuple(
            event
            for event in self._events
            if event.event_type == event_type
        )