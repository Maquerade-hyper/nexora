from dataclasses import dataclass
from typing import Any


WORKFLOW_SCHEMA_VERSION = 1

WORKFLOW_REQUIRED_FIELDS = (
    "schema_version",
    "id",
    "name",
    "description",
    "version",
    "graph",
)

GRAPH_REQUIRED_FIELDS = (
    "nodes",
    "ports",
    "edges",
)


@dataclass(frozen=True)
class NodeContract:
    id: str
    type: str
    config: dict[str, Any]


@dataclass(frozen=True)
class PortContract:
    id: str
    node_id: str
    name: str
    direction: str


@dataclass(frozen=True)
class EdgeContract:
    source_node_id: str
    source_port_id: str
    target_node_id: str
    target_port_id: str


@dataclass(frozen=True)
class WorkflowContract:
    schema_version: int
    id: str
    name: str
    description: str
    version: int