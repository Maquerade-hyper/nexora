from core.graph import Edge, Port, PortDirection
from core.nodes import NodeDefinition, NodeFactory, NodeRegistry
from core.nodes.instances.model import NodeInstance
from core.workflow.execution import (
    ExecutionContext,
    ExecutionControlStatus,
    ExecutionController,
    ExecutionEventType,
    ExecutionResult,
    InMemoryExecutionEventSink,
    NodeExecutor,
    NodeExecutorRegistry,
    WorkflowExecutionEngine,
)
from core.workflow.models import Workflow
from core.workflow.runs import WorkflowRun


class IntegrationExecutor(NodeExecutor):
    def __init__(self) -> None:
        self.calls: list[str] = []

    def execute(
        self,
        node: NodeInstance,
        context: ExecutionContext,
    ) -> ExecutionResult:
        self.calls.append(node.id)

        previous_outputs = dict(context.node_outputs)

        return ExecutionResult.succeeded(
            {
                "node_id": node.id,
                "previous_outputs": previous_outputs,
            }
        )


class IntegrationFailingExecutor(NodeExecutor):
    def execute(
        self,
        node: NodeInstance,
        context: ExecutionContext,
    ) -> ExecutionResult:
        return ExecutionResult.failed(
            "Integration failure"
        )


def create_registry() -> NodeRegistry:
    registry = NodeRegistry()

    registry.register(
        NodeDefinition(
            type="integration.node",
            name="Integration Node",
            description="Node used for V2 integration tests.",
            config_schema={},
        )
    )

    return registry


def create_workflow() -> Workflow:
    registry = create_registry()
    factory = NodeFactory(registry)

    workflow = Workflow(
        id="v2-integration",
        name="V2 Integration Workflow",
        description="Complete V2 execution test.",
    )

    node_a = factory.create(
        node_id="a",
        node_type="integration.node",
        config={},
    )

    node_b = factory.create(
        node_id="b",
        node_type="integration.node",
        config={},
    )

    workflow.graph.add_node(node_a)
    workflow.graph.add_node(node_b)

    workflow.graph.add_port(
        Port(
            id="a.output",
            node_id="a",
            name="output",
            direction=PortDirection.OUTPUT,
        )
    )

    workflow.graph.add_port(
        Port(
            id="b.input",
            node_id="b",
            name="input",
            direction=PortDirection.INPUT,
        )
    )

    workflow.graph.add_edge(
        Edge(
            source_node_id="a",
            source_port_id="a.output",
            target_node_id="b",
            target_port_id="b.input",
        )
    )

    return workflow


def test_v2_complete_execution_pipeline() -> None:
    workflow = create_workflow()

    executor = IntegrationExecutor()

    registry = NodeExecutorRegistry()
    registry.register(
        "integration.node",
        executor,
    )

    events = InMemoryExecutionEventSink()

    engine = WorkflowExecutionEngine(
        registry,
        events,
    )

    run = WorkflowRun(
        id="v2-run-1",
        workflow_id=workflow.id,
    )

    result = engine.execute(
        workflow,
        run,
    )

    assert result.status.value == "completed"

    assert result.nodes["a"].status.value == "completed"
    assert result.nodes["b"].status.value == "completed"

    assert executor.calls == ["a", "b"]

    event_types = [
        event.event_type
        for event in events.events
    ]

    assert event_types == [
        ExecutionEventType.WORKFLOW_STARTED,
        ExecutionEventType.NODE_READY,
        ExecutionEventType.NODE_STARTED,
        ExecutionEventType.NODE_COMPLETED,
        ExecutionEventType.NODE_READY,
        ExecutionEventType.NODE_STARTED,
        ExecutionEventType.NODE_COMPLETED,
        ExecutionEventType.WORKFLOW_COMPLETED,
    ]


def test_v2_failure_pipeline() -> None:
    workflow = create_workflow()

    registry = NodeExecutorRegistry()
    registry.register(
        "integration.node",
        IntegrationFailingExecutor(),
    )

    events = InMemoryExecutionEventSink()

    engine = WorkflowExecutionEngine(
        registry,
        events,
    )

    run = WorkflowRun(
        id="v2-failure",
        workflow_id=workflow.id,
    )

    result = engine.execute(
        workflow,
        run,
    )

    assert result.status.value == "failed"
    assert result.error == "Integration failure"

    assert result.nodes["a"].status.value == "failed"

    event_types = [
        event.event_type
        for event in events.events
    ]

    assert event_types == [
        ExecutionEventType.WORKFLOW_STARTED,
        ExecutionEventType.NODE_READY,
        ExecutionEventType.NODE_STARTED,
        ExecutionEventType.NODE_FAILED,
        ExecutionEventType.WORKFLOW_FAILED,
    ]


def test_v2_cancellation_pipeline() -> None:
    workflow = create_workflow()

    executor = IntegrationExecutor()

    registry = NodeExecutorRegistry()
    registry.register(
        "integration.node",
        executor,
    )

    events = InMemoryExecutionEventSink()

    controller = ExecutionController()
    controller.request_cancellation()

    engine = WorkflowExecutionEngine(
        registry,
        events,
    )

    run = WorkflowRun(
        id="v2-cancelled",
        workflow_id=workflow.id,
    )

    result = engine.execute(
        workflow,
        run,
        controller,
    )

    assert result.status.value == "cancelled"

    assert (
        controller.status
        == ExecutionControlStatus.CANCELLED
    )

    assert executor.calls == []

    assert [
        event.event_type
        for event in events.events
    ] == [
        ExecutionEventType.WORKFLOW_STARTED,
        ExecutionEventType.WORKFLOW_CANCELLED,
    ]