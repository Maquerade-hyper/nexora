from typing import Any

SENSITIVE_KEYS = frozenset(
    {
        "password",
        "passwd",
        "secret",
        "token",
        "access_token",
        "refresh_token",
        "api_key",
        "authorization",
        "private_key",
    }
)


def sanitize(data: dict[str, Any]) -> dict[str, Any]:
    """Redact sensitive values before they reach logs."""
    return {
        key: "[REDACTED]" if key.lower() in SENSITIVE_KEYS else value for key, value in data.items()
    }
