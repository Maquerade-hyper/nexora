import json
import logging

from runtime.observability.logging import (
    JsonFormatter,
    get_logger,
)


def test_logger() -> None:
    logger = get_logger("nexora.test")

    assert isinstance(logger, logging.Logger)
    assert logger.name == "nexora.test"


def test_json_formatter() -> None:
    formatter = JsonFormatter()

    record = logging.LogRecord(
        name="nexora.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="foundation test",
        args=(),
        exc_info=None,
    )

    output = formatter.format(record)
    payload = json.loads(output)

    assert payload["level"] == "INFO"
    assert payload["logger"] == "nexora.test"
    assert payload["message"] == "foundation test"
