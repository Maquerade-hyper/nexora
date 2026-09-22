from core.nodes.instances.model import NodeInstance
from core.workflow.execution.executor import NodeExecutor


class NodeExecutorRegistry:
    """Registry mapping node types to their executors."""

    def __init__(self) -> None:
        self._executors: dict[str, NodeExecutor] = {}

    def register(
        self,
        node_type: str,
        executor: NodeExecutor,
    ) -> None:
        if not node_type.strip():
            raise ValueError("Node type cannot be empty")

        if node_type in self._executors:
            raise ValueError(
                f"Executor already registered for node type: {node_type}"
            )

        self._executors[node_type] = executor

    def get(self, node: NodeInstance) -> NodeExecutor:
        node_type = node.type

        if node_type not in self._executors:
            raise KeyError(
                f"No executor registered for node type: {node_type}"
            )

        return self._executors[node_type]

    def exists(self, node_type: str) -> bool:
        return node_type in self._executors

    def count(self) -> int:
        return len(self._executors)