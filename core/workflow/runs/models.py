from dataclasses import dataclass, field
from enum import Enum


class WorkflowRunStatus(str, Enum):
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class NodeRunStatus(str, Enum):
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class NodeRun:
    node_id: str
    status: NodeRunStatus = NodeRunStatus.PENDING
    error: str | None = None

    def mark_ready(self) -> None:
        if self.status != NodeRunStatus.PENDING:
            raise ValueError(
                f"Node '{self.node_id}' cannot become ready "
                f"from status '{self.status.value}'."
            )

        self.status = NodeRunStatus.READY

    def mark_running(self) -> None:
        if self.status != NodeRunStatus.READY:
            raise ValueError(
                f"Node '{self.node_id}' cannot start running "
                f"from status '{self.status.value}'."
            )

        self.status = NodeRunStatus.RUNNING

    def mark_completed(self) -> None:
        if self.status != NodeRunStatus.RUNNING:
            raise ValueError(
                f"Node '{self.node_id}' cannot complete "
                f"from status '{self.status.value}'."
            )

        self.status = NodeRunStatus.COMPLETED

    def mark_failed(self, error: str) -> None:
        if self.status != NodeRunStatus.RUNNING:
            raise ValueError(
                f"Node '{self.node_id}' cannot fail "
                f"from status '{self.status.value}'."
            )

        if not error.strip():
            raise ValueError("Node failure error cannot be empty.")

        self.error = error
        self.status = NodeRunStatus.FAILED

    def mark_skipped(self) -> None:
        if self.status not in {
            NodeRunStatus.PENDING,
            NodeRunStatus.READY,
        }:
            raise ValueError(
                f"Node '{self.node_id}' cannot be skipped "
                f"from status '{self.status.value}'."
            )

        self.status = NodeRunStatus.SKIPPED


@dataclass
class WorkflowRun:
    id: str
    workflow_id: str
    status: WorkflowRunStatus = WorkflowRunStatus.PENDING
    nodes: dict[str, NodeRun] = field(default_factory=dict)
    error: str | None = None

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Workflow run ID cannot be empty.")

        if not self.workflow_id.strip():
            raise ValueError("Workflow ID cannot be empty.")