from core.workflow.runs.models import (
    NodeRun,
    NodeRunStatus,
    WorkflowRun,
    WorkflowRunStatus,
)

class WorkflowRunLifecycle:
    """Controls valid workflow-run lifecycle transitions."""

    def mark_ready(self, run: WorkflowRun) -> None:
        if run.status != WorkflowRunStatus.PENDING:
            raise ValueError(
                f"Workflow run cannot become ready "
                f"from status '{run.status.value}'."
            )

        run.status = WorkflowRunStatus.READY

    def mark_running(self, run: WorkflowRun) -> None:
        if run.status != WorkflowRunStatus.READY:
            raise ValueError(
                f"Workflow run cannot start running "
                f"from status '{run.status.value}'."
            )

        run.status = WorkflowRunStatus.RUNNING

    def mark_completed(self, run: WorkflowRun) -> None:
        if run.status != WorkflowRunStatus.RUNNING:
            raise ValueError(
                f"Workflow run cannot complete "
                f"from status '{run.status.value}'."
            )

        if any(
            node.status == NodeRunStatus.FAILED
            for node in run.nodes.values()
        ):
            raise ValueError(
                "Workflow run cannot complete while a node has failed."
            )

        run.status = WorkflowRunStatus.COMPLETED

    def mark_failed(self, run: WorkflowRun, error: str) -> None:
        if run.status != WorkflowRunStatus.RUNNING:
            raise ValueError(
                f"Workflow run cannot fail "
                f"from status '{run.status.value}'."
            )

        if not error.strip():
            raise ValueError("Workflow failure error cannot be empty.")

        run.error = error
        run.status = WorkflowRunStatus.FAILED

    def mark_cancelled(self, run: WorkflowRun) -> None:
        if run.status not in {
            WorkflowRunStatus.PENDING,
            WorkflowRunStatus.READY,
            WorkflowRunStatus.RUNNING,
        }:
            raise ValueError(
                f"Workflow run cannot be cancelled "
                f"from status '{run.status.value}'."
            )

        run.status = WorkflowRunStatus.CANCELLED

    def add_node(self, run: WorkflowRun, node_id: str) -> NodeRun:
        if not node_id.strip():
            raise ValueError("Node run ID cannot be empty.")

        if node_id in run.nodes:
            raise ValueError(
                f"Node run '{node_id}' already exists."
            )

        node_run = NodeRun(node_id=node_id)
        run.nodes[node_id] = node_run
        return node_run