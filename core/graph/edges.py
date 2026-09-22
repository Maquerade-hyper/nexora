from dataclasses import dataclass


@dataclass(frozen=True)
class Edge:
    """Connection between two workflow node ports."""

    source_node_id: str
    source_port_id: str
    target_node_id: str
    target_port_id: str

    def __post_init__(self) -> None:
        values = (
            self.source_node_id,
            self.source_port_id,
            self.target_node_id,
            self.target_port_id,
        )

        if any(not value.strip() for value in values):
            raise ValueError("Edge fields cannot be empty.")
