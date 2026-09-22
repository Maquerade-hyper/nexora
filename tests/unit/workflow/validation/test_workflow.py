import pytest

from core.graph import Edge, Port, PortDirection
from core.nodes import NodeDefinition, NodeInstance, NodeRegistry
from core.workflow.models import Workflow
from core.workflow.validation import (
    WorkflowValidationError,
    WorkflowValidator,
)


def create_registry() -> NodeRegistry:
    registry = NodeRegistry()

    registry.register(
        NodeDefinition(
            type="http.trigger",
            name="HTTP Trigger",
            description="Starts a workflow from HTTP.",
            config_schema={
                "required": ["method"],
                "properties": {
                    "method": {"type": "string"},
                },
            },
        )
    )

    registry.register(
        NodeDefinition(
            type="http.response",
            name="HTTP Response",
            description="Returns an HTTP response.",
            config_schema={
                "required": ["status"],
                "properties": {
                    "status": {"type": "integer"},
                },
            },
        )
    )

    return registry


def create_valid_workflow() -> Workflow:
    workflow = Workflow(
        id="workflow-1",
        name="HTTP Workflow",
        description="Valid workflow",
    )

    workflow.graph.add_node(
        NodeInstance(
            id="trigger",
            type="http.trigger",
            config={"method": "POST"},
        )
    )

    workflow.graph.add_node(
        NodeInstance(
            id="response",
            type="http.response",
            config={"status": 200},
        )
    )

    workflow.graph.add_port(
        Port(
            id="trigger.output",
            node_id="trigger",
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

    from core.graph import Edge

    workflow.graph.add_edge(
        Edge(
            source_node_id="trigger",
            source_port_id="trigger.output",
            target_node_id="response",
            target_port_id="response.input",
        )
    )

    return workflow


def test_valid_workflow_is_accepted() -> None:
    workflow = create_valid_workflow()
    validator = WorkflowValidator(create_registry())

    validator.validate(workflow)


def test_unknown_node_type_is_rejected() -> None:
    workflow = Workflow(
        id="workflow-1",
        name="Invalid Workflow",
        description="Unknown node",
    )

    workflow.graph.add_node(
        NodeInstance(
            id="unknown",
            type="unknown.node",
        )
    )

    validator = WorkflowValidator(create_registry())

    with pytest.raises(WorkflowValidationError, match="unknown node type"):
        validator.validate(workflow)


def test_invalid_node_configuration_is_rejected() -> None:
    workflow = Workflow(
        id="workflow-1",
        name="Invalid Workflow",
        description="Invalid configuration",
    )

    workflow.graph.add_node(
        NodeInstance(
            id="trigger",
            type="http.trigger",
            config={},
        )
    )

    validator = WorkflowValidator(create_registry())

    with pytest.raises(
        WorkflowValidationError,
        match="Missing required configuration fields",
    ):
        validator.validate(workflow)


def test_invalid_graph_is_rejected() -> None:
    workflow = Workflow(
        id="workflow-1",
        name="Invalid Workflow",
        description="Invalid graph",
    )

    workflow.graph.add_node(
        NodeInstance(
            id="trigger",
            type="http.trigger",
            config={"method": "POST"},
        )
    )

    from core.graph import Edge

    workflow.graph.add_edge(
        Edge(
            source_node_id="trigger",
            source_port_id="missing.output",
            target_node_id="missing",
            target_port_id="missing.input",
        )
    )

    validator = WorkflowValidator(create_registry())

    with pytest.raises(WorkflowValidationError):
        validator.validate(workflow)


def test_empty_workflow_id_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Workflow ID cannot be empty",
    ):
        Workflow(
            id="",
            name="Workflow",
            description="Test",
        )