import json
from typing import Any

from core.graph import WorkflowGraph
from core.workflow.models import Workflow


def serialize_graph(graph: WorkflowGraph) -> dict[str, Any]:
    return {
        "nodes": [
            {
                "id": node.id,
                "type": node.type,
                "config": node.config,
            }
            for node in graph.nodes
        ],
        "ports": [
            {
                "id": port.id,
                "node_id": port.node_id,
                "name": port.name,
                "direction": port.direction.value,
            }
            for port in graph.ports
        ],
        "edges": [
            {
                "source_node_id": edge.source_node_id,
                "source_port_id": edge.source_port_id,
                "target_node_id": edge.target_node_id,
                "target_port_id": edge.target_port_id,
            }
            for edge in graph.edges
        ],
    }


def serialize_workflow_json(workflow: Workflow) -> str:
    payload: dict[str, Any] = {
        "schema_version": 1,
        "id": workflow.id,
        "name": workflow.name,
        "description": workflow.description,
        "version": workflow.version,
        "graph": serialize_graph(workflow.graph),
    }

    return json.dumps(
        payload,
        indent=2,
        sort_keys=True,
    )