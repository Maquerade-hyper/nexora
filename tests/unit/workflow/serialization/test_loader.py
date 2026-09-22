import pytest

from core.graph import Edge, Port, PortDirection
from core.nodes import NodeInstance
from core.workflow.models import Workflow
from core.workflow.serialization import (
    WorkflowDeserializationError,
    deserialize_workflow_json,
    serialize_workflow_json,
)


def create_workflow() -> Workflow:
    workflow = Workflow(
        id="workflow-1",
        name="Registration",
        description="Registration workflow",
    )

    workflow.graph.add_node(
        NodeInstance(
            id="validate",
            type="validation",
            config={"required": ["email"]},
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

    workflow.graph.validate()

    return workflow


def test_workflow_can_round_trip_through_json() -> None:
    original = create_workflow()

    document = serialize_workflow_json(original)
    restored = deserialize_workflow_json(document)

    assert restored.id == original.id
    assert restored.name == original.name
    assert restored.description == original.description
    assert restored.version == original.version

    assert restored.graph.node_count() == 2
    assert restored.graph.edge_count() == 1

    validate_node = restored.graph.node("validate")

    assert validate_node is not None
    assert validate_node.type == "validation"
    assert validate_node.config == {"required": ["email"]}


def test_invalid_json_is_rejected() -> None:
    with pytest.raises(WorkflowDeserializationError):
        deserialize_workflow_json("{invalid}")


def test_unsupported_schema_version_is_rejected() -> None:
    document = """
    {
        "schema_version": 99,
        "id": "workflow-1",
        "name": "Test",
        "description": "Test",
        "version": 1,
        "graph": {
            "nodes": [],
            "ports": [],
            "edges": []
        }
    }
    """

    with pytest.raises(WorkflowDeserializationError):
        deserialize_workflow_json(document)


def test_invalid_graph_connection_is_rejected() -> None:
    document = """
    {
        "schema_version": 1,
        "id": "workflow-1",
        "name": "Test",
        "description": "Test",
        "version": 1,
        "graph": {
            "nodes": [
                {
                    "id": "node-a",
                    "type": "test"
                }
            ],
            "ports": [],
            "edges": [
                {
                    "source_node_id": "node-a",
                    "source_port_id": "missing",
                    "target_node_id": "node-a",
                    "target_port_id": "missing"
                }
            ]
        }
    }
    """

    with pytest.raises(Exception):
        deserialize_workflow_json(document)