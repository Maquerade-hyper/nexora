from runtime.observability.logging.sanitize import sanitize


def test_sensitive_values_are_redacted() -> None:
    result = sanitize(
        {
            "username": "gunesh",
            "password": "secret123",
            "api_key": "abc",
            "token": "xyz",
        }
    )

    assert result["username"] == "gunesh"
    assert result["password"] == "[REDACTED]"
    assert result["api_key"] == "[REDACTED]"
    assert result["token"] == "[REDACTED]"


def test_non_sensitive_values_are_preserved() -> None:
    result = sanitize(
        {
            "username": "gunesh",
            "environment": "development",
        }
    )

    assert result["username"] == "gunesh"
    assert result["environment"] == "development"
