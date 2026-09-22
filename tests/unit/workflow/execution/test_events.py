from core.workflow.execution import (
    ExecutionEvent,
    ExecutionEventType,
    InMemoryExecutionEventSink,
)


def create_event(
    event_type: ExecutionEventType,
    node_id: str | None = None,
) -> ExecutionEvent:
    return ExecutionEvent(
        event_type=event_type,
        workflow_id="workflow-1",
        run_id="run-1",
        node_id=node_id,
    )


def test_event_sink_stores_events() -> None:
    sink = InMemoryExecutionEventSink()

    event = create_event(
        ExecutionEventType.WORKFLOW_STARTED,
    )

    sink.emit(event)

    assert sink.events == (event,)


def test_event_sink_preserves_order() -> None:
    sink = InMemoryExecutionEventSink()

    first = create_event(
        ExecutionEventType.WORKFLOW_STARTED,
    )

    second = create_event(
        ExecutionEventType.NODE_STARTED,
        "node-a",
    )

    sink.emit(first)
    sink.emit(second)

    assert sink.events == (first, second)


def test_event_sink_filters_by_type() -> None:
    sink = InMemoryExecutionEventSink()

    sink.emit(
        create_event(
            ExecutionEventType.NODE_STARTED,
            "node-a",
        )
    )

    sink.emit(
        create_event(
            ExecutionEventType.NODE_COMPLETED,
            "node-a",
        )
    )

    sink.emit(
        create_event(
            ExecutionEventType.NODE_STARTED,
            "node-b",
        )
    )

    events = sink.by_type(
        ExecutionEventType.NODE_STARTED,
    )

    assert len(events) == 2
    assert events[0].node_id == "node-a"
    assert events[1].node_id == "node-b"


def test_event_sink_clear() -> None:
    sink = InMemoryExecutionEventSink()

    sink.emit(
        create_event(
            ExecutionEventType.WORKFLOW_STARTED,
        )
    )

    sink.clear()

    assert sink.events == ()