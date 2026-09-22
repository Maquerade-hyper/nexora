from core.nodes.models import NodeDefinition


class NodeRegistry:
    """Registry of available Nexora node definitions."""

    def __init__(self) -> None:
        self._definitions: dict[str, NodeDefinition] = {}

    def register(self, definition: NodeDefinition) -> None:
        """Register a node definition."""

        if definition.type in self._definitions:
            raise ValueError(f"Node type '{definition.type}' is already registered.")

        self._definitions[definition.type] = definition

    def get(self, node_type: str) -> NodeDefinition:
        """Return a registered node definition."""

        try:
            return self._definitions[node_type]
        except KeyError as exc:
            raise KeyError(f"Node type '{node_type}' is not registered.") from exc

    def exists(self, node_type: str) -> bool:
        """Return whether a node type is registered."""

        return node_type in self._definitions

    def all(self) -> tuple[NodeDefinition, ...]:
        """Return all registered node definitions."""

        return tuple(self._definitions[node_type] for node_type in sorted(self._definitions))

    def count(self) -> int:
        """Return the number of registered node types."""

        return len(self._definitions)
