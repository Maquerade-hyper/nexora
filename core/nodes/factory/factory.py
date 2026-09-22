from typing import Any

from core.nodes.instances import NodeInstance
from core.nodes.registry import NodeRegistry


class NodeFactory:
    """Creates concrete node instances from registered definitions."""

    def __init__(self, registry: NodeRegistry) -> None:
        self._registry = registry

    def create(
        self,
        *,
        node_id: str,
        node_type: str,
        config: dict[str, Any] | None = None,
    ) -> NodeInstance:
        """Create a node instance from a registered node definition."""

        definition = self._registry.get(node_type)
        node_config = dict(config or {})

        return NodeInstance(
            id=node_id,
            type=definition.type,
            config=node_config,
        )
