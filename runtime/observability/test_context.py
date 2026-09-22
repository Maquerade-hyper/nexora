from runtime.observability.context.context import (
    clear_context,
    correlation_id,
    request_id,
    set_context,
)


def test_context_values() -> None:
    set_context(
        request="req-123",
        correlation="corr-123",
    )

    assert request_id.get() == "req-123"
    assert correlation_id.get() == "corr-123"


def test_context_can_be_cleared() -> None:
    set_context(
        request="req-123",
        correlation="corr-123",
    )

    clear_context()

    assert request_id.get() is None
    assert correlation_id.get() is None
