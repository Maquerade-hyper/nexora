from dataclasses import dataclass, field
from typing import Any

from core.graph.ports import Port


@dataclass(frozen=True)
class NodeDefinition:
    """Definition of a reusable Nexora node."""

    type: str
    name: str
    description: str
    version: int = 1
    inputs: tuple[Port, ...] = field(default_factory=tuple)
    outputs: tuple[Port, ...] = field(default_factory=tuple)
    config_schema: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.type.strip():
            raise ValueError("Node type cannot be empty.")

        if not self.name.strip():
            raise ValueError("Node name cannot be empty.")

        if self.version < 1:
            raise ValueError("Node version must be at least 1.")
