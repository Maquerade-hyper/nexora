from enum import Enum


class ExecutionControlStatus(str, Enum):
    """Control state for a workflow execution."""

    ACTIVE = "active"
    CANCEL_REQUESTED = "cancel_requested"
    CANCELLED = "cancelled"


class ExecutionController:
    """Controls cancellation state for one workflow execution."""

    def __init__(self) -> None:
        self._status = ExecutionControlStatus.ACTIVE

    @property
    def status(self) -> ExecutionControlStatus:
        return self._status

    @property
    def cancellation_requested(self) -> bool:
        return (
            self._status
            == ExecutionControlStatus.CANCEL_REQUESTED
        )

    def request_cancellation(self) -> None:
        if self._status == ExecutionControlStatus.CANCELLED:
            return

        self._status = ExecutionControlStatus.CANCEL_REQUESTED

    def mark_cancelled(self) -> None:
        if self._status != ExecutionControlStatus.CANCEL_REQUESTED:
            raise RuntimeError(
                "Execution cancellation was not requested"
            )

        self._status = ExecutionControlStatus.CANCELLED