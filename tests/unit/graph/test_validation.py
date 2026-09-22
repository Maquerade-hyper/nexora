import pytest

from core.errors.graph import DuplicateNodeError, InvalidConnectionError
from core.graph.edges import Edge
from core.graph.graph import WorkflowGraph
from core.graph.models import Node
from core.graph.ports import Port, PortDirection


def test_duplicate_nodes_are_rejected() -> None:
    graph = WorkflowGraph()

    graph.add_node(
        Node(
            id="node-1",
            type="test",
            name="Node One",
        )
    )

    graph.add_node(
        Node(
            id="node-1",
            type="test",
            name="Duplicate Node",
        )
    )

    with pytest.raises(DuplicateNodeError):
        graph.validate()


def test_invalid_port_direction_is_rejected() -> None:
    graph = WorkflowGraph()

    graph.add_node(
        Node(
            id="source",
            type="test",
            name="Source",
        )
    )

    graph.add_node(
        Node(
            id="target",
            type="test",
            name="Target",
        )
    )

    graph.add_port(
        Port(
            id="source.input",
            node_id="source",
            name="input",
            direction=PortDirection.INPUT,
        )
    )

    graph.add_port(
        Port(
            id="target.input",
            node_id="target",
            name="input",
            direction=PortDirection.INPUT,
        )
    )

    graph.add_edge(
        Edge(
            source_node_id="source",
            source_port_id="source.input",
            target_node_id="target",
            target_port_id="target.input",
        )
    )

    with pytest.raises(InvalidConnectionError):
        graph.validate()
