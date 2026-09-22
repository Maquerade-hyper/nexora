from abc import ABC, abstractmethod

from core.nodes.instances.model import NodeInstance
from core.workflow.execution.context import ExecutionContext
from core.workflow.execution.result import ExecutionResult


class NodeExecutor(ABC):
    """Contract for executing a Nexora node."""

    @abstractmethod
    def execute(
        self,
        node: NodeInstance,
        context: ExecutionContext,
    ) -> ExecutionResult:
        """Execute a node using the supplied execution context."""
        raise NotImplementedError