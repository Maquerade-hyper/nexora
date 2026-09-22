import json
from dataclasses import asdict

from core.workflow.models import Workflow


def serialize_workflow(workflow: Workflow) -> str:
    """Serialize a workflow into JSON."""

    workflow.validate()

    return json.dumps(
        asdict(workflow),
        indent=2,
        sort_keys=True,
    )
