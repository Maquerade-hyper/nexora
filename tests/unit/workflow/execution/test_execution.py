from core.workflow.execution import (
    ExecutionContext,
    ExecutionResult,
)


def test_execution_context_stores_output() -> None:
    context = ExecutionContext(
        workflow_id="workflow-1",
        run_id="run-1",
    )

    context.set_output("node-1", {"value": 42})

    assert context.has_output("node-1")
    assert context.get_output("node-1") == {"value": 42}


def test_execution_context_missing_output() -> None:
    context = ExecutionContext(
        workflow_id="workflow-1",
        run_id="run-1",
    )

    assert not context.has_output("node-1")


def test_successful_execution_result() -> None:
    result = ExecutionResult.succeeded({"value": 42})

    assert result.success
    assert result.output == {"value": 42}
    assert result.error is None


def test_failed_execution_result() -> None:
    result = ExecutionResult.failed("Something went wrong")

    assert not result.success
    assert result.output is None
    assert result.error == "Something went wrong"