import pytest

from core.graph import Edge, Port, PortDirection
from core.nodes import NodeInstance
from core.workflow.models import Workflow
from core.workflow.planning import (
    WorkflowPlanner,
    WorkflowPlanningError,
)


def create_node_graph(
    node_ids: list[str],
    edges: list[Edge],
) -> Workflow:
    workflow = Workflow(
        id="workflow-1",
        name="Planning Test",
        description="Execution planning test",
    )

    for node_id in node_ids:
        workflow.graph.add_node(
            NodeInstance(
                id=node_id,
                type="test.node",
            )
        )

    for edge in edges:
        workflow.graph.add_edge(edge)

    return workflow


def test_linear_workflow_produces_deterministic_order() -> None:
    workflow = create_node_graph(
        ["response", "trigger", "validate"],
        [
            Edge(
                source_node_id="trigger",
                source_port_id="trigger.output",
                target_node_id="validate",
                target_port_id="validate.input",
            ),
            Edge(
                source_node_id="validate",
                source_port_id="validate.output",
                target_node_id="response",
                target_port_id="response.input",
            ),
        ],
    )

    planner = WorkflowPlanner()
    plan = planner.create_plan(workflow)

    assert plan.node_ids == (
        "trigger",
        "validate",
        "response",
    )


def test_parallel_nodes_can_be_planned() -> None:
    workflow = create_node_graph(
        ["final", "first", "second"],
        [
            Edge(
                source_node_id="first",
                source_port_id="first.output",
                target_node_id="final",
                target_port_id="final.input",
            ),
            Edge(
                source_node_id="second",
                source_port_id="second.output",
                target_node_id="final",
                target_port_id="final.input",
            ),
        ],
    )

    planner = WorkflowPlanner()
    plan = planner.create_plan(workflow)

    assert plan.node_ids == (
        "first",
        "second",
        "final",
    )

    final_step = plan.steps[-1]

    assert final_step.node_id == "final"
    assert final_step.dependencies == (
        "first",
        "second",
    )


def test_independent_nodes_are_ordered_deterministically() -> None:
    workflow = create_node_graph(
        ["z-node", "a-node", "m-node"],
        [],
    )

    planner = WorkflowPlanner()
    plan = planner.create_plan(workflow)

    assert plan.node_ids == (
        "a-node",
        "m-node",
        "z-node",
    )


def test_dependency_cycle_is_rejected() -> None:
    workflow = create_node_graph(
        ["a", "b", "c"],
        [
            Edge(
                source_node_id="a",
                source_port_id="a.output",
                target_node_id="b",
                target_port_id="b.input",
            ),
            Edge(
                source_node_id="b",
                source_port_id="b.output",
                target_node_id="c",
                target_port_id="c.input",
            ),
            Edge(
                source_node_id="c",
                source_port_id="c.output",
                target_node_id="a",
                target_port_id="a.input",
            ),
        ],
    )

    planner = WorkflowPlanner()

    with pytest.raises(
        WorkflowPlanningError,
        match="dependency cycle",
    ):
        planner.create_plan(workflow)


def test_missing_source_node_is_rejected() -> None:
    workflow = create_node_graph(
        ["target"],
        [
            Edge(
                source_node_id="missing",
                source_port_id="missing.output",
                target_node_id="target",
                target_port_id="target.input",
            )
        ],
    )

    planner = WorkflowPlanner()

    with pytest.raises(
        WorkflowPlanningError,
        match="Source node",
    ):
        planner.create_plan(workflow)


def test_missing_target_node_is_rejected() -> None:
    workflow = create_node_graph(
        ["source"],
        [
            Edge(
                source_node_id="source",
                source_port_id="source.output",
                target_node_id="missing",
                target_port_id="missing.input",
            )
        ],
    )

    planner = WorkflowPlanner()

    with pytest.raises(
        WorkflowPlanningError,
        match="Target node",
    ):
        planner.create_plan(workflow)


def test_execution_steps_contain_dependencies() -> None:
    workflow = create_node_graph(
        ["trigger", "database", "response"],
        [
            Edge(
                source_node_id="trigger",
                source_port_id="trigger.output",
                target_node_id="database",
                target_port_id="database.input",
            ),
            Edge(
                source_node_id="database",
                source_port_id="database.output",
                target_node_id="response",
                target_port_id="response.input",
            ),
        ],
    )

    planner = WorkflowPlanner()
    plan = planner.create_plan(workflow)

    assert plan.steps[0].node_id == "trigger"
    assert plan.steps[0].dependencies == ()

    assert plan.steps[1].node_id == "database"
    assert plan.steps[1].dependencies == ("trigger",)

    assert plan.steps[2].node_id == "response"
    assert plan.steps[2].dependencies == ("database",)