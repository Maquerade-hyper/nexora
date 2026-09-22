from dataclasses import dataclass, field

from core.graph.edges import Edge
from core.graph.models import Node
from core.graph.ports import Port
from core.graph.validation import validate_edges, validate_nodes


@dataclass
class WorkflowGraph:
    """In-memory representation of a Nexora workflow graph."""

    nodes: list[Node] = field(default_factory=list)
    ports: list[Port] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)

    def add_node(self, node: Node) -> None:
        self.nodes.append(node)

    def add_port(self, port: Port) -> None:
        self.ports.append(port)

    def add_edge(self, edge: Edge) -> None:
        self.edges.append(edge)

    def validate(self) -> None:
        validate_nodes(self.nodes)
        validate_edges(self.nodes, self.ports, self.edges)

    def node(self, node_id: str) -> Node | None:
        for node in self.nodes:
            if node.id == node_id:
                return node

        return None
