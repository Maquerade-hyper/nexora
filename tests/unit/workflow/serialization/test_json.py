import json

from core.graph import Edge, Port, PortDirection
from core.nodes import NodeInstance
from core.workflow.models import Workflow
from core.workflow.serialization import serialize_workflow_json


def test_workflow_can_be_serialized_with_graph_details() -> None:
    workflow = Workflow(
        id="workflow-1",
        name="Registration",
        description="User registration workflow",
    )

    workflow.graph.add_node(
        NodeInstance(
            id="validate",
            type="validation",
            config={"required": ["email", "password"]},
        )
    )

    workflow.graph.add_node(
        NodeInstance(
            id="response",
            type="http.response",
            config={"status": 201},
        )
    )

    workflow.graph.add_port(
        Port(
            id="validate.output",
            node_id="validate",
            name="output",
            direction=PortDirection.OUTPUT,
        )
    )

    workflow.graph.add_port(
        Port(
            id="response.input",
            node_id="response",
            name="input",
            direction=PortDirection.INPUT,
        )
    )

    workflow.graph.add_edge(
        Edge(
            source_node_id="validate",
            source_port_id="validate.output",
            target_node_id="response",
            target_port_id="response.input",
        )
    )

    document = serialize_workflow_json(workflow)
    data = json.loads(document)

    assert data["schema_version"] == 1
    assert data["id"] == "workflow-1"
    assert data["name"] == "Registration"
    assert len(data["graph"]["nodes"]) == 2
    assert len(data["graph"]["ports"]) == 2
    assert len(data["graph"]["edges"]) == 1