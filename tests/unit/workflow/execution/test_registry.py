from core.nodes import NodeDefinition, NodeFactory, NodeRegistry
from core.nodes.instances.model import NodeInstance
from core.workflow.execution import (
    ExecutionContext,
    ExecutionResult,
    NodeExecutor,
    NodeExecutorRegistry,
)


class TestExecutor(NodeExecutor):
    def execute(
        self,
        node: NodeInstance,
        context: ExecutionContext,
    ) -> ExecutionResult:
        return ExecutionResult.succeeded(
            {"node_id": node.id}
        )


def create_node() -> NodeInstance:
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

    return factory.create(
        node_id="node-1",
        node_type="test.node",
        config={},
    )


def test_executor_registry_registers_executor() -> None:
    registry = NodeExecutorRegistry()
    executor = TestExecutor()

    registry.register("test.node", executor)

    assert registry.exists("test.node")
    assert registry.count() == 1


def test_executor_registry_returns_executor() -> None:
    registry = NodeExecutorRegistry()
    executor = TestExecutor()

    registry.register("test.node", executor)

    node = create_node()

    assert registry.get(node) is executor


def test_executor_registry_rejects_duplicate() -> None:
    registry = NodeExecutorRegistry()

    registry.register("test.node", TestExecutor())

    try:
        registry.register("test.node", TestExecutor())
        assert False
    except ValueError:
        assert True