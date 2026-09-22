from core.workflow.planning.plan import ExecutionPlan


class DependencyResolver:
    """Determines which execution steps are ready to run."""

    def __init__(self, plan: ExecutionPlan) -> None:
        self._plan = plan

    def dependencies_for(
        self,
        node_id: str,
    ) -> tuple[str, ...]:
        for step in self._plan.steps:
            if step.node_id == node_id:
                return step.dependencies

        raise KeyError(
            f"Node not found in execution plan: {node_id}"
        )

    def are_satisfied(
        self,
        node_id: str,
        completed_nodes: set[str],
    ) -> bool:
        dependencies = self.dependencies_for(node_id)

        return all(
            dependency in completed_nodes
            for dependency in dependencies
        )

    def ready_nodes(
        self,
        completed_nodes: set[str],
        running_nodes: set[str],
    ) -> tuple[str, ...]:
        ready: list[str] = []

        for step in self._plan.steps:
            node_id = step.node_id

            if node_id in completed_nodes:
                continue

            if node_id in running_nodes:
                continue

            if self.are_satisfied(
                node_id,
                completed_nodes,
            ):
                ready.append(node_id)

        return tuple(ready)