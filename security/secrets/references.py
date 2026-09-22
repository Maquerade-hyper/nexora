from dataclasses import dataclass


@dataclass(frozen=True)
class SecretReference:
    """Reference to a secret without containing its value."""

    name: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Secret reference name cannot be empty.")

    def __str__(self) -> str:
        return self.name
