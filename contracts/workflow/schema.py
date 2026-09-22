from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class NodeContract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    type: str
    name: str
    config: dict[str, Any] = Field(default_factory=dict)


class PortContract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    node_id: str
    name: str
    direction: str


class EdgeContract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_node_id: str
    source_port_id: str
    target_node_id: str
    target_port_id: str


class WorkflowContract(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    description: str = ""
    version: int = 1
    nodes: list[NodeContract] = Field(default_factory=list)
    ports: list[PortContract] = Field(default_factory=list)
    edges: list[EdgeContract] = Field(default_factory=list)
