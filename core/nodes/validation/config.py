from typing import Any

from core.nodes.models import NodeDefinition
from core.nodes.instances import NodeInstance


class NodeConfigurationError(ValueError):
    """Raised when a node instance configuration is invalid."""


def validate_node_configuration(
    node: NodeInstance,
    definition: NodeDefinition,
) -> None:
    if node.type != definition.type:
        raise NodeConfigurationError(
            f"Node type '{node.type}' does not match "
            f"definition type '{definition.type}'."
        )

    schema = definition.config_schema

    if not schema:
        return

    required = schema.get("required", [])

    if not isinstance(required, list):
        raise NodeConfigurationError(
            "Node configuration schema 'required' must be a list."
        )

    missing = [
        field
        for field in required
        if field not in node.config
    ]

    if missing:
        raise NodeConfigurationError(
            "Missing required configuration fields: "
            + ", ".join(sorted(missing))
        )

    properties = schema.get("properties", {})

    if not isinstance(properties, dict):
        raise NodeConfigurationError(
            "Node configuration schema 'properties' must be an object."
        )

    for field, rules in properties.items():
        if field not in node.config:
            continue

        if not isinstance(rules, dict):
            raise NodeConfigurationError(
                f"Configuration rules for '{field}' must be an object."
            )

        expected_type = rules.get("type")

        if expected_type is None:
            continue

        value = node.config[field]

        if expected_type == "string" and not isinstance(value, str):
            raise NodeConfigurationError(
                f"Configuration field '{field}' must be a string."
            )

        if expected_type == "integer" and (
            not isinstance(value, int) or isinstance(value, bool)
        ):
            raise NodeConfigurationError(
                f"Configuration field '{field}' must be an integer."
            )

        if expected_type == "number" and (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
        ):
            raise NodeConfigurationError(
                f"Configuration field '{field}' must be a number."
            )

        if expected_type == "boolean" and not isinstance(value, bool):
            raise NodeConfigurationError(
                f"Configuration field '{field}' must be a boolean."
            )

        if expected_type == "object" and not isinstance(value, dict):
            raise NodeConfigurationError(
                f"Configuration field '{field}' must be an object."
            )

        if expected_type == "array" and not isinstance(value, list):
            raise NodeConfigurationError(
                f"Configuration field '{field}' must be an array."
            )