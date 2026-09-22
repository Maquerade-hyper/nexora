from typing import Any


def validate_config_type(config: Any) -> None:
    """Validate the basic configuration container."""

    if not isinstance(config, dict):
        raise TypeError("Node configuration must be a dictionary.")
