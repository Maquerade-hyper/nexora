from security.policies.security import SecurityPolicy


def test_security_policy_defaults_to_safe_values() -> None:
    policy = SecurityPolicy()

    assert policy.allow_plaintext_secrets is False
    assert policy.allow_secret_logging is False
    assert policy.require_secret_references is True
    assert policy.require_explicit_permissions is True
    assert policy.default_deny is True
