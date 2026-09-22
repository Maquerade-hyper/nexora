class GraphError(Exception):
    """Base exception for workflow graph errors."""


class DuplicateNodeError(GraphError):
    """Raised when a graph contains duplicate node IDs."""


class NodeNotFoundError(GraphError):
    """Raised when a referenced node does not exist."""


class InvalidConnectionError(GraphError):
    """Raised when an edge connects invalid ports."""


class DuplicateConnectionError(GraphError):
    """Raised when an identical connection already exists."""
