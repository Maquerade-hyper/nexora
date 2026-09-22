from dataclasses import dataclass, field

from core.errors.graph import (
    DuplicateConnectionError,
    InvalidConnectionError,
    NodeNotFoundError,
)
from core.nodes import (
    NodeConfigurationError,
    NodeRegistry,
    validate_node_configuration,
)
from core.workflow.models import Workflow


class WorkflowValidationError(ValueError):
    """Raised when a complete workflow is invalid."""


@dataclass
class WorkflowValidator:
    registry: NodeRegistry
    errors: list[str] = field(default_factory=list)

    def validate(self, workflow: Workflow) -> None:
        self.errors.clear()

        self._validate_workflow_metadata(workflow)
        self._validate_graph(workflow)
        self._validate_nodes(workflow)

        if self.errors:
            message = "Workflow validation failed:\n" + "\n".join(
                f"- {error}" for error in self.errors
            )
            raise WorkflowValidationError(message)

    def _validate_workflow_metadata(self, workflow: Workflow) -> None:
        if not workflow.id.strip():
            self.errors.append("Workflow ID cannot be empty.")

        if not workflow.name.strip():
            self.errors.append("Workflow name cannot be empty.")

        if workflow.version < 1:
            self.errors.append("Workflow version must be at least 1.")

    def _validate_graph(self, workflow: Workflow) -> None:
        try:
            workflow.graph.validate()
        except (
            DuplicateConnectionError,
            InvalidConnectionError,
            NodeNotFoundError,
        ) as exc:
            self.errors.append(str(exc))

    def _validate_nodes(self, workflow: Workflow) -> None:
        for node in workflow.graph.nodes:
            try:
                definition = self.registry.get(node.type)
            except KeyError:
                self.errors.append(
                    f"Node '{node.id}' uses unknown node type "
                    f"'{node.type}'."
                )
                continue

            try:
                validate_node_configuration(node, definition)
            except NodeConfigurationError as exc:
                self.errors.append(
                    f"Node '{node.id}': {exc}"
                )