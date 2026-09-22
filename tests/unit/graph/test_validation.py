import pytest

from core.errors.graph import (
    DuplicateNodeError,
    InvalidConnectionError,
)
from core.graph import Edge, Port, PortDirection, WorkflowGraph
from core.nodes import NodeInstance


def test_duplicate_nodes_are_rejected() -> None:
    graph = WorkflowGraph()

    graph.add_node(
        NodeInstance(
            id="node-1",
            type="test",
        )
    )

    with pytest.raises(DuplicateNodeError):
        graph.add_node(
            NodeInstance(
                id="node-1",
                type="test",
            )
        )


def test_invalid_port_direction_is_rejected() -> None:
    graph = WorkflowGraph()

    graph.add_node(
        NodeInstance(
            id="source",
            type="test",
        )
    )

    graph.add_node(
        NodeInstance(
            id="target",
            type="test",
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
