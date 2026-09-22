import json
from typing import Any

from core.graph import Edge, Port, PortDirection, WorkflowGraph
from core.nodes import NodeInstance
from core.workflow.models import Workflow


class WorkflowDeserializationError(ValueError):
    """Raised when a workflow JSON document cannot be reconstructed."""


def _require(payload: dict[str, Any], key: str) -> Any:
    if key not in payload:
        raise WorkflowDeserializationError(
            f"Missing required field: '{key}'."
        )
    return payload[key]


def deserialize_graph(payload: dict[str, Any]) -> WorkflowGraph:
    nodes_data = _require(payload, "nodes")
    ports_data = _require(payload, "ports")
    edges_data = _require(payload, "edges")

    if not isinstance(nodes_data, list):
        raise WorkflowDeserializationError("'nodes' must be a list.")

    if not isinstance(ports_data, list):
        raise WorkflowDeserializationError("'ports' must be a list.")

    if not isinstance(edges_data, list):
        raise WorkflowDeserializationError("'edges' must be a list.")

    graph = WorkflowGraph()

    for node_data in nodes_data:
        if not isinstance(node_data, dict):
            raise WorkflowDeserializationError(
                "Each node must be an object."
            )

        graph.add_node(
            NodeInstance(
                id=_require(node_data, "id"),
                type=_require(node_data, "type"),
                config=node_data.get("config", {}),
            )
        )

    for port_data in ports_data:
        if not isinstance(port_data, dict):
            raise WorkflowDeserializationError(
                "Each port must be an object."
            )

        try:
            direction = PortDirection(
                _require(port_data, "direction")
            )
        except ValueError as exc:
            raise WorkflowDeserializationError(
                "Invalid port direction."
            ) from exc

        graph.add_port(
            Port(
                id=_require(port_data, "id"),
                node_id=_require(port_data, "node_id"),
                name=_require(port_data, "name"),
                direction=direction,
            )
        )

    for edge_data in edges_data:
        if not isinstance(edge_data, dict):
            raise WorkflowDeserializationError(
                "Each edge must be an object."
            )

        graph.add_edge(
            Edge(
                source_node_id=_require(edge_data, "source_node_id"),
                source_port_id=_require(edge_data, "source_port_id"),
                target_node_id=_require(edge_data, "target_node_id"),
                target_port_id=_require(edge_data, "target_port_id"),
            )
        )

    graph.validate()
    return graph


def deserialize_workflow_json(document: str) -> Workflow:
    try:
        payload = json.loads(document)
    except json.JSONDecodeError as exc:
        raise WorkflowDeserializationError(
            "Workflow document contains invalid JSON."
        ) from exc

    if not isinstance(payload, dict):
        raise WorkflowDeserializationError(
            "Workflow document must contain a JSON object."
        )

    schema_version = _require(payload, "schema_version")

    if schema_version != 1:
        raise WorkflowDeserializationError(
            f"Unsupported workflow schema version: {schema_version}."
        )

    workflow = Workflow(
        id=_require(payload, "id"),
        name=_require(payload, "name"),
        description=_require(payload, "description"),
        version=_require(payload, "version"),
    )

    workflow.graph = deserialize_graph(
        _require(payload, "graph")
    )

    return workflow