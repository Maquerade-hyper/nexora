from core.workflow.models import Workflow
from core.workflow.planning.plan import ExecutionPlan, ExecutionStep


class WorkflowPlanningError(ValueError):
    """Raised when an execution plan cannot be created."""


class WorkflowPlanner:
    """Builds a deterministic execution plan from a workflow graph."""

    def create_plan(self, workflow: Workflow) -> ExecutionPlan:
        graph = workflow.graph

        node_ids = {node.id for node in graph.nodes}

        dependencies: dict[str, set[str]] = {
            node_id: set() for node_id in node_ids
        }

        for edge in graph.edges:
            if edge.source_node_id not in node_ids:
                raise WorkflowPlanningError(
                    f"Source node '{edge.source_node_id}' does not exist."
                )

            if edge.target_node_id not in node_ids:
                raise WorkflowPlanningError(
                    f"Target node '{edge.target_node_id}' does not exist."
                )

            dependencies[edge.target_node_id].add(
                edge.source_node_id
            )

        remaining = {
            node_id: set(node_dependencies)
            for node_id, node_dependencies in dependencies.items()
        }

        ordered: list[str] = []

        while remaining:
            ready = sorted(
                node_id
                for node_id, node_dependencies in remaining.items()
                if not node_dependencies
            )

            if not ready:
                cycle_nodes = ", ".join(sorted(remaining))
                raise WorkflowPlanningError(
                    f"Workflow contains a dependency cycle involving: "
                    f"{cycle_nodes}."
                )

            for node_id in ready:
                ordered.append(node_id)
                del remaining[node_id]

            for node_dependencies in remaining.values():
                node_dependencies.difference_update(ready)

        steps = tuple(
            ExecutionStep(
                node_id=node_id,
                dependencies=tuple(
                    sorted(dependencies[node_id])
                ),
            )
            for node_id in ordered
        )

        return ExecutionPlan(steps=steps)