from abc import ABC, abstractmethod
from typing import Any

from core.nodes.models import NodeDefinition


class NodeDefinitionProvider(ABC):
    """Base interface for providers of node definitions."""

    @abstractmethod
    def definition(self) -> NodeDefinition:
        """Return the node definition."""
        raise NotImplementedError

    def validate_config(self, config: dict[str, Any]) -> None:
        """Validate node configuration.

        Detailed schema validation will be implemented later.
        """
        if not isinstance(config, dict):
            raise TypeError("Node configuration must be a dictionary.")
