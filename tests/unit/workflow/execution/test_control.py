import pytest

from core.workflow.execution import (
    ExecutionControlStatus,
    ExecutionController,
)


def test_controller_starts_active() -> None:
    controller = ExecutionController()

    assert controller.status == ExecutionControlStatus.ACTIVE
    assert not controller.cancellation_requested


def test_cancellation_can_be_requested() -> None:
    controller = ExecutionController()

    controller.request_cancellation()

    assert (
        controller.status
        == ExecutionControlStatus.CANCEL_REQUESTED
    )
    assert controller.cancellation_requested


def test_cancellation_can_be_completed() -> None:
    controller = ExecutionController()

    controller.request_cancellation()
    controller.mark_cancelled()

    assert controller.status == ExecutionControlStatus.CANCELLED


def test_cancellation_requires_request() -> None:
    controller = ExecutionController()

    with pytest.raises(RuntimeError):
        controller.mark_cancelled()


def test_cancelled_execution_stays_cancelled() -> None:
    controller = ExecutionController()

    controller.request_cancellation()
    controller.mark_cancelled()
    controller.request_cancellation()

    assert controller.status == ExecutionControlStatus.CANCELLED