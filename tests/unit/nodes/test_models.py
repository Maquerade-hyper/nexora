import pytest

from core.nodes.models import NodeDefinition


def test_node_definition_can_be_created() -> None:
    definition = NodeDefinition(
        type="http.trigger",
        name="HTTP Trigger",
        description="Starts a workflow from an HTTP request.",
    )

    assert definition.type == "http.trigger"
    assert definition.name == "HTTP Trigger"
    assert definition.version == 1
    assert definition.inputs == ()
    assert definition.outputs == ()


def test_node_definition_requires_type() -> None:
    with pytest.raises(ValueError):
        NodeDefinition(
            type="",
            name="HTTP Trigger",
            description="HTTP trigger node.",
        )


def test_node_definition_requires_name() -> None:
    with pytest.raises(ValueError):
        NodeDefinition(
            type="http.trigger",
            name="",
            description="HTTP trigger node.",
        )


def test_node_definition_version_must_be_positive() -> None:
    with pytest.raises(ValueError):
        NodeDefinition(
            type="http.trigger",
            name="HTTP Trigger",
            description="HTTP trigger node.",
            version=0,
        )
