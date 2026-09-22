from core.graph import Edge, Port, PortDirection, WorkflowGraph
from core.nodes import NodeInstance


def test_workflow_graph_can_contain_node_instances_and_edges() -> None:
    graph = WorkflowGraph()

    trigger = NodeInstance(
        id="trigger",
        type="http.trigger",
    )

    response = NodeInstance(
        id="response",
        type="http.response",
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
    assert graph.node_count() == 2
    assert graph.edge_count() == 1
