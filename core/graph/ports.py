from dataclasses import dataclass
from enum import Enum


class PortDirection(str, Enum):
    INPUT = "input"
    OUTPUT = "output"


@dataclass(frozen=True)
class Port:
    """Input or output port belonging to a node."""

    id: str
    node_id: str
    name: str
    direction: PortDirection

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Port ID cannot be empty.")

        if not self.node_id.strip():
            raise ValueError("Port node ID cannot be empty.")

        if not self.name.strip():
            raise ValueError("Port name cannot be empty.")
