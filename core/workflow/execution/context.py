from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExecutionContext:
    """Runtime data shared by nodes during one workflow run."""

    workflow_id: str
    run_id: str
    node_outputs: dict[str, Any] = field(default_factory=dict)

    def set_output(
        self,
        node_id: str,
        output: Any,
    ) -> None:
        if not node_id.strip():
            raise ValueError("Node ID cannot be empty")

        self.node_outputs[node_id] = output

    def get_output(
        self,
        node_id: str,
    ) -> Any:
        if node_id not in self.node_outputs:
            raise KeyError(
                f"No output available for node: {node_id}"
            )

        return self.node_outputs[node_id]

    def has_output(
        self,
        node_id: str,
    ) -> bool:
        return node_id in self.node_outputs

    def get_outputs(
        self,
        node_ids: list[str],
    ) -> dict[str, Any]:
        return {
            node_id: self.get_output(node_id)
            for node_id in node_ids
        }