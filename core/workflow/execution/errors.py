class ExecutionError(Exception):
    """Base exception for workflow execution errors."""


class NodeExecutionError(ExecutionError):
    """Raised when a node cannot be executed."""


class WorkflowExecutionError(ExecutionError):
    """Raised when workflow execution fails."""