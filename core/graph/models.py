from dataclasses import dataclass, field
from typing import Any


@dataclass
class Node:
    """A generic node in a Nexora workflow."""

    id: str
    type: str
    name: str
    config: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Node ID cannot be empty.")

        if not self.type.strip():
            raise ValueError("Node type cannot be empty.")

        if not self.name.strip():
            raise ValueError("Node name cannot be empty.")
