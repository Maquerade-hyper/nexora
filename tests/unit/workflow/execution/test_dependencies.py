from core.workflow.execution import DependencyResolver
from core.workflow.planning import (
    ExecutionPlan,
    ExecutionStep,
)


def create_plan() -> ExecutionPlan:
    return ExecutionPlan(
        steps=(
            ExecutionStep(
                node_id="a",
                dependencies=(),
            ),
            ExecutionStep(
                node_id="b",
                dependencies=("a",),
            ),
            ExecutionStep(
                node_id="c",
                dependencies=("a",),
            ),
            ExecutionStep(
                node_id="d",
                dependencies=("b", "c"),
            ),
        )
    )


def test_root_node_is_ready() -> None:
    resolver = DependencyResolver(create_plan())

    ready = resolver.ready_nodes(
        completed_nodes=set(),
        running_nodes=set(),
    )

    assert ready == ("a",)


def test_dependent_nodes_become_ready() -> None:
    resolver = DependencyResolver(create_plan())

    ready = resolver.ready_nodes(
        completed_nodes={"a"},
        running_nodes=set(),
    )

    assert ready == ("b", "c")


def test_join_node_waits_for_all_dependencies() -> None:
    resolver = DependencyResolver(create_plan())

    ready = resolver.ready_nodes(
        completed_nodes={"a", "b"},
        running_nodes=set(),
    )

    assert "d" not in ready

    ready = resolver.ready_nodes(
        completed_nodes={"a", "b", "c"},
        running_nodes=set(),
    )

    assert ready == ("d",)


def test_completed_nodes_are_not_ready() -> None:
    resolver = DependencyResolver(create_plan())

    ready = resolver.ready_nodes(
        completed_nodes={"a"},
        running_nodes=set(),
    )

    assert "a" not in ready