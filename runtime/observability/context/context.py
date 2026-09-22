from contextvars import ContextVar

request_id: ContextVar[str | None] = ContextVar(
    "request_id",
    default=None,
)

correlation_id: ContextVar[str | None] = ContextVar(
    "correlation_id",
    default=None,
)

workflow_id: ContextVar[str | None] = ContextVar(
    "workflow_id",
    default=None,
)

node_id: ContextVar[str | None] = ContextVar(
    "node_id",
    default=None,
)


def set_context(
    *,
    request: str | None = None,
    correlation: str | None = None,
    workflow: str | None = None,
    node: str | None = None,
) -> None:
    """Set identifiers for the current execution context."""
    request_id.set(request)
    correlation_id.set(correlation)
    workflow_id.set(workflow)
    node_id.set(node)


def clear_context() -> None:
    """Clear the current execution context."""
    request_id.set(None)
    correlation_id.set(None)
    workflow_id.set(None)
    node_id.set(None)
