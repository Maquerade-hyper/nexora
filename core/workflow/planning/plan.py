from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionStep:
    node_id: str
    dependencies: tuple[str, ...]


@dataclass(frozen=True)
class ExecutionPlan:
    steps: tuple[ExecutionStep, ...]

    @property
    def node_ids(self) -> tuple[str, ...]:
        return tuple(step.node_id for step in self.steps)