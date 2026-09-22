import pytest

from core.workflow.runs import (
    NodeRunStatus,
    WorkflowRun,
    WorkflowRunLifecycle,
    WorkflowRunStatus,
)


def create_run() -> WorkflowRun:
    return WorkflowRun(
        id="run-1",
        workflow_id="workflow-1",
    )


def test_workflow_run_starts_pending() -> None:
    run = create_run()

    assert run.status == WorkflowRunStatus.PENDING
    assert run.nodes == {}


def test_workflow_run_can_move_to_ready() -> None:
    run = create_run()
    lifecycle = WorkflowRunLifecycle()

    lifecycle.mark_ready(run)

    assert run.status == WorkflowRunStatus.READY


def test_workflow_run_can_move_to_running() -> None:
    run = create_run()
    lifecycle = WorkflowRunLifecycle()

    lifecycle.mark_ready(run)
    lifecycle.mark_running(run)

    assert run.status == WorkflowRunStatus.RUNNING


def test_workflow_run_can_complete() -> None:
    run = create_run()
    lifecycle = WorkflowRunLifecycle()

    lifecycle.mark_ready(run)
    lifecycle.mark_running(run)
    lifecycle.mark_completed(run)

    assert run.status == WorkflowRunStatus.COMPLETED


def test_workflow_run_can_fail() -> None:
    run = create_run()
    lifecycle = WorkflowRunLifecycle()

    lifecycle.mark_ready(run)
    lifecycle.mark_running(run)
    lifecycle.mark_failed(run, "Database unavailable.")

    assert run.status == WorkflowRunStatus.FAILED
    assert run.error == "Database unavailable."


def test_workflow_run_can_be_cancelled() -> None:
    run = create_run()
    lifecycle = WorkflowRunLifecycle()

    lifecycle.mark_ready(run)
    lifecycle.mark_cancelled(run)

    assert run.status == WorkflowRunStatus.CANCELLED


def test_invalid_workflow_transition_is_rejected() -> None:
    run = create_run()
    lifecycle = WorkflowRunLifecycle()

    with pytest.raises(ValueError, match="cannot start running"):
        lifecycle.mark_running(run)


def test_node_run_lifecycle() -> None:
    run = create_run()
    lifecycle = WorkflowRunLifecycle()

    node = lifecycle.add_node(run, "database")

    assert node.status.value == "pending"

    node.mark_ready()
    assert node.status.name == "READY"

    node.mark_running()
    assert node.status.name == "RUNNING"

    node.mark_completed()
    assert node.status.name == "COMPLETED"


def test_failed_node_prevents_workflow_completion() -> None:
    run = create_run()
    lifecycle = WorkflowRunLifecycle()

    node = lifecycle.add_node(run, "database")

    lifecycle.mark_ready(run)
    lifecycle.mark_running(run)

    node.mark_ready()
    node.mark_running()
    node.mark_failed("Connection failed.")

    with pytest.raises(
        ValueError,
        match="while a node has failed",
    ):
        lifecycle.mark_completed(run)


def test_failed_node_requires_error_message() -> None:
    run = create_run()
    lifecycle = WorkflowRunLifecycle()

    node = lifecycle.add_node(run, "database")

    node.mark_ready()
    node.mark_running()

    with pytest.raises(
        ValueError,
        match="error cannot be empty",
    ):
        node.mark_failed("")


def test_duplicate_node_runs_are_rejected() -> None:
    run = create_run()
    lifecycle = WorkflowRunLifecycle()

    lifecycle.add_node(run, "database")

    with pytest.raises(
        ValueError,
        match="already exists",
    ):
        lifecycle.add_node(run, "database")