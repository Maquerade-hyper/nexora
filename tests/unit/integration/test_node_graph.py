from core.graph import Edge, Port, PortDirection, WorkflowGraph
from core.nodes import NodeDefinition, NodeFactory, NodeRegistry


def test_factory_created_nodes_can_be_added_to_graph() -> None:
    registry = NodeRegistry()

    registry.register(
        NodeDefinition(
            type="http.trigger",
            name="HTTP Trigger",
            description="Starts a workflow from HTTP.",
        )
    )

    registry.register(
        NodeDefinition(
            type="http.response",
            name="HTTP Response",
            description="Returns an HTTP response.",
        )
    )

    factory = NodeFactory(registry)
    graph = WorkflowGraph()

    trigger = factory.create(
        node_id="trigger-1",
        node_type="http.trigger",
        config={"method": "POST"},
    )

    response = factory.create(
        node_id="response-1",
        node_type="http.response",
    )

    graph.add_node(trigger)
    graph.add_node(response)

    graph.add_port(
        Port(
            id="trigger-1.output",
            node_id="trigger-1",
            name="output",
            direction=PortDirection.OUTPUT,
        )
    )

    graph.add_port(
        Port(
            id="response-1.input",
            node_id="response-1",
            name="input",
            direction=PortDirection.INPUT,
        )
    )

    graph.add_edge(
        Edge(
            source_node_id="trigger-1",
            source_port_id="trigger-1.output",
            target_node_id="response-1",
            target_port_id="response-1.input",
        )
    )

    graph.validate()

    assert graph.node_count() == 2
    assert graph.edge_count() == 1
    assert graph.node("trigger-1") is trigger
    assert graph.node("response-1") is response
