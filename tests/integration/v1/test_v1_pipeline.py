from core.graph import Edge, Port, PortDirection
from core.nodes import (
    NodeDefinition,
    NodeFactory,
    NodeRegistry,
)
from core.workflow.planning import WorkflowPlanner
from core.workflow.runs import (
    WorkflowRun,
    WorkflowRunLifecycle,
    WorkflowRunStatus,
)
from core.workflow.serialization import (
    deserialize_workflow_json,
    serialize_workflow_json,
)
from core.workflow.validation import WorkflowValidator
from core.workflow.models import Workflow


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
            type="database.query",
            name="Database Query",
            description="Executes a database query.",
            config_schema={
                "required": ["query"],
                "properties": {
                    "query": {"type": "string"},
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


def create_workflow(registry: NodeRegistry) -> Workflow:
    factory = NodeFactory(registry)

    workflow = Workflow(
        id="user-registration",
        name="User Registration",
        description="Registration backend workflow",
    )

    trigger = factory.create(
        node_id="trigger",
        node_type="http.trigger",
        config={"method": "POST"},
    )

    database = factory.create(
        node_id="database",
        node_type="database.query",
        config={"query": "SELECT * FROM users"},
    )

    response = factory.create(
        node_id="response",
        node_type="http.response",
        config={"status": 200},
    )

    workflow.graph.add_node(trigger)
    workflow.graph.add_node(database)
    workflow.graph.add_node(response)

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
            id="database.input",
            node_id="database",
            name="input",
            direction=PortDirection.INPUT,
        )
    )

    workflow.graph.add_port(
        Port(
            id="database.output",
            node_id="database",
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
            source_node_id="trigger",
            source_port_id="trigger.output",
            target_node_id="database",
            target_port_id="database.input",
        )
    )

    workflow.graph.add_edge(
        Edge(
            source_node_id="database",
            source_port_id="database.output",
            target_node_id="response",
            target_port_id="response.input",
        )
    )

    return workflow


def test_complete_v1_workflow_pipeline() -> None:
    registry = create_registry()

    workflow = create_workflow(registry)

    validator = WorkflowValidator(registry)
    validator.validate(workflow)

    document = serialize_workflow_json(workflow)

    restored = deserialize_workflow_json(document)

    validator.validate(restored)

    planner = WorkflowPlanner()
    plan = planner.create_plan(restored)

    assert plan.node_ids == (
        "trigger",
        "database",
        "response",
    )

    run = WorkflowRun(
        id="run-1",
        workflow_id=restored.id,
    )

    lifecycle = WorkflowRunLifecycle()

    for step in plan.steps:
        lifecycle.add_node(run, step.node_id)

    lifecycle.mark_ready(run)
    lifecycle.mark_running(run)

    assert run.status == WorkflowRunStatus.RUNNING
    assert set(run.nodes) == {
        "trigger",
        "database",
        "response",
    }

    for node_run in run.nodes.values():
        node_run.mark_ready()
        node_run.mark_running()
        node_run.mark_completed()

    lifecycle.mark_completed(run)

    assert run.status.value == "completed"

    for node_run in run.nodes.values():
        assert node_run.status.value == "completed"