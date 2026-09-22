from dataclasses import dataclass, field

from core.errors.graph import DuplicateNodeError, NodeNotFoundError
from core.graph.edges import Edge
from core.graph.ports import Port
from core.graph.validation import validate_edges
from core.nodes.instances import NodeInstance


@dataclass
class WorkflowGraph:
    """In-memory representation of a Nexora workflow graph."""

    nodes: list[NodeInstance] = field(default_factory=list)
    ports: list[Port] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)

    def add_node(self, node: NodeInstance) -> None:
        """Add a node instance to the graph."""

        if self.node(node.id) is not None:
            raise DuplicateNodeError(f"Node '{node.id}' is already present in the graph.")

        self.nodes.append(node)

    def remove_node(self, node_id: str) -> NodeInstance:
        """Remove a node and its connected edges."""

        node = self.node(node_id)

        if node is None:
            raise NodeNotFoundError(f"Node '{node_id}' does not exist.")

        self.nodes.remove(node)

        self.edges = [
            edge
            for edge in self.edges
            if edge.source_node_id != node_id and edge.target_node_id != node_id
        ]

        self.ports = [port for port in self.ports if port.node_id != node_id]

        return node

    def add_port(self, port: Port) -> None:
        """Add a port to the graph."""

        self.ports.append(port)

    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph."""

        self.edges.append(edge)

    def validate(self) -> None:
        """Validate the complete graph."""

        validate_edges(
            self.nodes,
            self.ports,
            self.edges,
        )

    def node(self, node_id: str) -> NodeInstance | None:
        """Find a node instance by ID."""

        for node in self.nodes:
            if node.id == node_id:
                return node

        return None

    def node_count(self) -> int:
        """Return the number of nodes."""

        return len(self.nodes)

    def edge_count(self) -> int:
        """Return the number of edges."""

        return len(self.edges)
