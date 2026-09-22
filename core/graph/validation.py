from core.errors.graph import (
    DuplicateConnectionError,
    DuplicateNodeError,
    InvalidConnectionError,
    NodeNotFoundError,
)
from core.graph.edges import Edge
from core.graph.models import Node
from core.graph.ports import Port, PortDirection


def validate_nodes(nodes: list[Node]) -> None:
    """Validate node identity and uniqueness."""

    seen: set[str] = set()

    for node in nodes:
        if node.id in seen:
            raise DuplicateNodeError(f"Node '{node.id}' is defined more than once.")

        seen.add(node.id)


def validate_edges(
    nodes: list[Node],
    ports: list[Port],
    edges: list[Edge],
) -> None:
    """Validate graph connections."""

    node_ids = {node.id for node in nodes}
    port_map = {port.id: port for port in ports}
    connections: set[tuple[str, str, str, str]] = set()

    for edge in edges:
        if edge.source_node_id not in node_ids:
            raise NodeNotFoundError(f"Source node '{edge.source_node_id}' does not exist.")

        if edge.target_node_id not in node_ids:
            raise NodeNotFoundError(f"Target node '{edge.target_node_id}' does not exist.")

        source_port = port_map.get(edge.source_port_id)
        target_port = port_map.get(edge.target_port_id)

        if source_port is None:
            raise InvalidConnectionError(f"Source port '{edge.source_port_id}' does not exist.")

        if target_port is None:
            raise InvalidConnectionError(f"Target port '{edge.target_port_id}' does not exist.")

        if source_port.node_id != edge.source_node_id:
            raise InvalidConnectionError(
                f"Source port '{edge.source_port_id}' belongs to "
                f"node '{source_port.node_id}', not '{edge.source_node_id}'."
            )

        if target_port.node_id != edge.target_node_id:
            raise InvalidConnectionError(
                f"Target port '{edge.target_port_id}' belongs to "
                f"node '{target_port.node_id}', not '{edge.target_node_id}'."
            )

        if source_port.direction != PortDirection.OUTPUT:
            raise InvalidConnectionError(
                f"Source port '{edge.source_port_id}' must be an output port."
            )

        if target_port.direction != PortDirection.INPUT:
            raise InvalidConnectionError(
                f"Target port '{edge.target_port_id}' must be an input port."
            )

        connection_key = (
            edge.source_node_id,
            edge.source_port_id,
            edge.target_node_id,
            edge.target_port_id,
        )

        if connection_key in connections:
            raise DuplicateConnectionError("The connection already exists.")

        connections.add(connection_key)
