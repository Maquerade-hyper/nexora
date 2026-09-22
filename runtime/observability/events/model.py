from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class RuntimeEvent:
    event_type: str
    message: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    workflow_id: str | None = None
    node_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
