from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ExecutionResult:
    """Result produced by a node execution."""

    success: bool
    output: Any = None
    error: str | None = None

    @classmethod
    def succeeded(cls, output: Any = None) -> "ExecutionResult":
        return cls(
            success=True,
            output=output,
        )

    @classmethod
    def failed(cls, error: str) -> "ExecutionResult":
        if not error.strip():
            raise ValueError("Execution error cannot be empty")

        return cls(
            success=False,
            error=error,
        )