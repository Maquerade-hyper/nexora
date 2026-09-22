from core.graph.edges import Edge
from core.graph.graph import WorkflowGraph
from core.graph.models import Node
from core.graph.ports import Port, PortDirection


def test_workflow_graph_can_contain_nodes_and_edges() -> None:
    graph = WorkflowGraph()

    trigger = Node(
        id="trigger",
        type="http.trigger",
        name="HTTP Trigger",
    )

    response = Node(
        id="response",
        type="http.response",
        name="HTTP Response",
    )

    graph.add_node(trigger)
    graph.add_node(response)

    graph.add_port(
        Port(
            id="trigger.output",
            node_id="trigger",
            name="output",
            direction=PortDirection.OUTPUT,
        )
    )

    graph.add_port(
        Port(
            id="response.input",
            node_id="response",
            name="input",
            direction=PortDirection.INPUT,
        )
    )

    graph.add_edge(
        Edge(
            source_node_id="trigger",
            source_port_id="trigger.output",
            target_node_id="response",
            target_port_id="response.input",
        )
    )

    graph.validate()

    assert graph.node("trigger") is trigger
    assert graph.node("response") is response
    assert len(graph.edges) == 1
