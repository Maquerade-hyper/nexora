from collections.abc import Mapping

from security.secrets.references import SecretReference


class SecretManager:
    """In-memory secret manager foundation.

    This is intentionally a development foundation.
    Production secret providers will be implemented through
    adapters in later versions.
    """

    def __init__(self, secrets: Mapping[str, str] | None = None) -> None:
        self._secrets: dict[str, str] = dict(secrets or {})

    def set(self, name: str, value: str) -> None:
        """Store a secret under a reference name."""
        if not name.strip():
            raise ValueError("Secret name cannot be empty.")

        self._secrets[name] = value

    def get(self, reference: SecretReference) -> str:
        """Resolve a secret reference."""
        try:
            return self._secrets[reference.name]
        except KeyError as exc:
            raise KeyError(f"Secret '{reference.name}' was not found.") from exc

    def exists(self, reference: SecretReference) -> bool:
        """Check whether a secret exists."""
        return reference.name in self._secrets

    def delete(self, reference: SecretReference) -> None:
        """Delete a secret."""
        self._secrets.pop(reference.name, None)

    def names(self) -> tuple[str, ...]:
        """Return secret names without exposing secret values."""
        return tuple(sorted(self._secrets))
