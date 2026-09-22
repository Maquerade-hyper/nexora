from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityPolicy:
    """Baseline Nexora security policy."""

    allow_plaintext_secrets: bool = False
    allow_secret_logging: bool = False
    require_secret_references: bool = True
    require_explicit_permissions: bool = True
    default_deny: bool = True
