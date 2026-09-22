import pytest

from core.nodes.models import NodeDefinition
from core.nodes.registry import NodeRegistry


def make_definition(node_type: str) -> NodeDefinition:
    return NodeDefinition(
        type=node_type,
        name=node_type.replace(".", " ").title(),
        description="Test node.",
    )


def test_registry_can_register_node() -> None:
    registry = NodeRegistry()

    definition = make_definition("http.trigger")

    registry.register(definition)

    assert registry.exists("http.trigger")
    assert registry.get("http.trigger") is definition
    assert registry.count() == 1


def test_registry_rejects_duplicate_node_types() -> None:
    registry = NodeRegistry()

    registry.register(make_definition("http.trigger"))

    with pytest.raises(ValueError):
        registry.register(make_definition("http.trigger"))


def test_registry_rejects_unknown_node_type() -> None:
    registry = NodeRegistry()

    with pytest.raises(KeyError):
        registry.get("unknown.node")


def test_registry_returns_sorted_definitions() -> None:
    registry = NodeRegistry()

    registry.register(make_definition("database.query"))
    registry.register(make_definition("http.trigger"))

    definitions = registry.all()

    assert [definition.type for definition in definitions] == [
        "database.query",
        "http.trigger",
    ]
