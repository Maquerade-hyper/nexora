from dataclasses import dataclass, field
from typing import Any


@dataclass
class NodeInstance:
    """A concrete node placed inside a Nexora workflow."""

    id: str
    type: str
    config: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Node instance ID cannot be empty.")

        if not self.type.strip():
            raise ValueError("Node instance type cannot be empty.")

        if not isinstance(self.config, dict):
            raise TypeError("Node instance configuration must be a dictionary.")
