from core.graph import Edge, Port, PortDirection
from core.nodes import NodeDefinition, NodeFactory, NodeRegistry
from core.nodes.instances.model import NodeInstance
from core.workflow.execution import (
    ExecutionContext,
    ExecutionControlStatus,
    ExecutionController,
    ExecutionResult,
    NodeExecutor,
    NodeExecutorRegistry,
    WorkflowExecutionEngine,
)
from core.workflow.models import Workflow
from core.workflow.runs import WorkflowRun


class RecordingExecutor(NodeExecutor):
    def __init__(self, calls: list[str]) -> None:
        self.calls = calls

    def execute(
        self,
        node: NodeInstance,
        context: ExecutionContext,
    ) -> ExecutionResult:
        self.calls.append(node.id)

        return ExecutionResult.succeeded(
            {
                "node": node.id,
                "executed": True,
            }
        )


class FailingExecutor(NodeExecutor):
    def execute(
        self,
        node: NodeInstance,
        context: ExecutionContext,
    ) -> ExecutionResult:
        return ExecutionResult.failed(
            "Intentional test failure"
        )


class RaisingExecutor(NodeExecutor):
    def execute(
        self,
        node: NodeInstance,
        context: ExecutionContext,
    ) -> ExecutionResult:
        raise RuntimeError("Unexpected executor error")


def create_workflow() -> Workflow:
    registry = NodeRegistry()

    registry.register(
        NodeDefinition(
            type="test.node",
            name="Test Node",
            description="Test execution node.",
            config_schema={},
        )
    )

    factory = NodeFactory(registry)

    workflow = Workflow(
        id="workflow-1",
        name="Execution Test",
        description="Tests workflow execution.",
    )

    node_a = factory.create(
        node_id="a",
        node_type="test.node",
        config={},
    )

    node_b = factory.create(
        node_id="b",
        node_type="test.node",
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


def test_engine_executes_workflow() -> None:
    workflow = create_workflow()

    calls: list[str] = []

    registry = NodeExecutorRegistry()

    registry.register(
        "test.node",
        RecordingExecutor(calls),
    )

    engine = WorkflowExecutionEngine(registry)

    run = WorkflowRun(
        id="run-1",
        workflow_id=workflow.id,
    )

    result = engine.execute(
        workflow,
        run,
    )

    assert result.id == "run-1"
    assert result.workflow_id == "workflow-1"
    assert result.status.value == "completed"

    assert result.nodes["a"].status.value == "completed"
    assert result.nodes["b"].status.value == "completed"

    assert calls == ["a", "b"]


def test_engine_handles_node_failure() -> None:
    workflow = create_workflow()

    registry = NodeExecutorRegistry()

    registry.register(
        "test.node",
        FailingExecutor(),
    )

    engine = WorkflowExecutionEngine(registry)

    run = WorkflowRun(
        id="run-failure",
        workflow_id=workflow.id,
    )

    result = engine.execute(
        workflow,
        run,
    )

    assert result.status.value == "failed"
    assert result.error == "Intentional test failure"
    assert result.nodes["a"].status.value == "failed"


def test_engine_handles_cancellation() -> None:
    workflow = create_workflow()

    calls: list[str] = []

    registry = NodeExecutorRegistry()

    registry.register(
        "test.node",
        RecordingExecutor(calls),
    )

    controller = ExecutionController()
    controller.request_cancellation()

    engine = WorkflowExecutionEngine(registry)

    run = WorkflowRun(
        id="run-cancelled",
        workflow_id=workflow.id,
    )

    result = engine.execute(
        workflow,
        run,
        controller,
    )

    assert result.status.value == "cancelled"
    assert calls == []
    assert controller.status == ExecutionControlStatus.CANCELLED


def test_engine_handles_executor_exception() -> None:
    workflow = create_workflow()

    registry = NodeExecutorRegistry()

    registry.register(
        "test.node",
        RaisingExecutor(),
    )

    engine = WorkflowExecutionEngine(registry)

    run = WorkflowRun(
        id="run-exception",
        workflow_id=workflow.id,
    )

    result = engine.execute(
        workflow,
        run,
    )

    assert result.status.value == "failed"
    assert result.error == "Unexpected executor error"
    assert result.nodes["a"].status.value == "failed"