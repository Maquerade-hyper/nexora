import json

from core.nodes import NodeInstance
from core.workflow.models import Workflow
from core.workflow.workflow import serialize_workflow


def test_workflow_can_be_serialized() -> None:
    workflow = Workflow(
        id="workflow-1",
        name="User Registration",
        description="Basic registration workflow",
    )

    workflow.graph.add_node(
        NodeInstance(
            id="validate",
            type="validation",
            config={"required": ["email", "password"]},
        )
    )

    serialized = serialize_workflow(workflow)
    data = json.loads(serialized)

    assert data["id"] == "workflow-1"
    assert data["name"] == "User Registration"
    assert data["version"] == 1
    assert len(data["graph"]["nodes"]) == 1
