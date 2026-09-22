import pytest

from core.nodes import (
    NodeConfigurationError,
    NodeDefinition,
    NodeInstance,
    validate_node_configuration,
)


def create_definition() -> NodeDefinition:
    return NodeDefinition(
        type="database.query",
        name="Database Query",
        description="Executes a database query.",
        config_schema={
            "required": ["connection", "query"],
            "properties": {
                "connection": {"type": "string"},
                "query": {"type": "string"},
                "timeout": {"type": "integer"},
                "enabled": {"type": "boolean"},
            },
        },
    )


def test_valid_configuration_is_accepted() -> None:
    definition = create_definition()

    node = NodeInstance(
        id="query-1",
        type="database.query",
        config={
            "connection": "postgres",
            "query": "SELECT * FROM users",
            "timeout": 30,
            "enabled": True,
        },
    )

    validate_node_configuration(node, definition)


def test_missing_required_configuration_is_rejected() -> None:
    definition = create_definition()

    node = NodeInstance(
        id="query-1",
        type="database.query",
        config={
            "connection": "postgres",
        },
    )

    with pytest.raises(NodeConfigurationError, match="query"):
        validate_node_configuration(node, definition)


def test_wrong_string_type_is_rejected() -> None:
    definition = create_definition()

    node = NodeInstance(
        id="query-1",
        type="database.query",
        config={
            "connection": 123,
            "query": "SELECT * FROM users",
        },
    )

    with pytest.raises(NodeConfigurationError, match="connection"):
        validate_node_configuration(node, definition)


def test_wrong_integer_type_is_rejected() -> None:
    definition = create_definition()

    node = NodeInstance(
        id="query-1",
        type="database.query",
        config={
            "connection": "postgres",
            "query": "SELECT * FROM users",
            "timeout": "30",
        },
    )

    with pytest.raises(NodeConfigurationError, match="timeout"):
        validate_node_configuration(node, definition)


def test_wrong_boolean_type_is_rejected() -> None:
    definition = create_definition()

    node = NodeInstance(
        id="query-1",
        type="database.query",
        config={
            "connection": "postgres",
            "query": "SELECT * FROM users",
            "enabled": "true",
        },
    )

    with pytest.raises(NodeConfigurationError, match="enabled"):
        validate_node_configuration(node, definition)


def test_node_type_must_match_definition() -> None:
    definition = create_definition()

    node = NodeInstance(
        id="query-1",
        type="http.request",
        config={
            "connection": "postgres",
            "query": "SELECT * FROM users",
        },
    )

    with pytest.raises(NodeConfigurationError, match="does not match"):
        validate_node_configuration(node, definition)


def test_empty_schema_accepts_configuration() -> None:
    definition = NodeDefinition(
        type="custom.node",
        name="Custom Node",
        description="Custom node.",
    )

    node = NodeInstance(
        id="custom-1",
        type="custom.node",
        config={"anything": "value"},
    )

    validate_node_configuration(node, definition)