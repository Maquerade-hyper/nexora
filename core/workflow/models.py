from dataclasses import dataclass, field

from core.graph.graph import WorkflowGraph


@dataclass
class Workflow:
    """A complete Nexora workflow."""

    id: str
    name: str
    description: str = ""
    version: int = 1
    graph: WorkflowGraph = field(default_factory=WorkflowGraph)

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Workflow ID cannot be empty.")

        if not self.name.strip():
            raise ValueError("Workflow name cannot be empty.")

        if self.version < 1:
            raise ValueError("Workflow version must be at least 1.")

    def validate(self) -> None:
        self.graph.validate()
