import pytest

from security.secrets import SecretManager, SecretReference


def test_secret_can_be_stored_and_resolved() -> None:
    manager = SecretManager()

    reference = SecretReference("database.production")

    manager.set(reference.name, "super-secret")

    assert manager.get(reference) == "super-secret"


def test_secret_reference_does_not_contain_value() -> None:
    reference = SecretReference("stripe.production")

    assert reference.name == "stripe.production"
    assert "secret" not in reference.name.lower()


def test_missing_secret_raises_error() -> None:
    manager = SecretManager()

    reference = SecretReference("missing.secret")

    with pytest.raises(KeyError):
        manager.get(reference)


def test_secret_names_do_not_expose_values() -> None:
    manager = SecretManager(
        {
            "database.production": "database-password",
            "stripe.production": "stripe-key",
        }
    )

    assert manager.names() == (
        "database.production",
        "stripe.production",
    )

    assert "database-password" not in manager.names()
    assert "stripe-key" not in manager.names()


def test_secret_can_be_deleted() -> None:
    manager = SecretManager()

    reference = SecretReference("temporary.secret")

    manager.set(reference.name, "value")

    assert manager.exists(reference)

    manager.delete(reference)

    assert not manager.exists(reference)
