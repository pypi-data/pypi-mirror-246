import copy
import logging
import os
import re
from unittest.mock import patch
from urllib.parse import urlparse

import pytest

_log = logging.getLogger(__name__)


def get_db_details():
    db_url = urlparse(os.environ.get("SQLALCHEMY_DATABASE_URI"))
    _log.debug(f"db_url: {mask_password(db_url.geturl())}")
    dbname = db_url.path[1:]
    user = db_url.username
    password = db_url.password
    host = db_url.hostname
    port = db_url.port

    return dbname, user, password, host, port


def mask_password(db_url: str) -> str:
    """replaces password with ***
    BETTER: use URL class from sqlalchemy to parse the uri

    \\1 refers to group 1, and \\3 refers to group 3.
    replaces the entire match with the contents of group 1, followed by ***, followed by the contents of group 3.

    equivalent:
    pattern = r"(.*:.+:)(.+)(@.*)"
    return re.sub(pattern, "\\1****\\3", uri)
    """
    return re.sub(r"://([^:]+):([^@]+)", r"://\1:****", db_url)


def sanitize_cloudwatch_event(event: dict) -> dict:
    sanitized_event = copy.deepcopy(event)
    if "DB_PASSWORD" in sanitized_event:
        sanitized_event["DB_PASSWORD"] = "*" * len(sanitized_event["DB_PASSWORD"])
    return sanitized_event


################################################################################
# Tests
################################################################################
# A list of test cases with corresponding expected results
test_cases = [
    (
        "postgresql://username:password@localhost:5432/dbname",
        ("dbname", "username", "password", "localhost", 5432),
    ),
    ("mysql://user:pass@localhost:3306/db", ("db", "user", "pass", "localhost", 3306)),
    ("sqlite:///path/to/db.sqlite", ("path/to/db.sqlite", None, None, None, None)),
]


@pytest.mark.parametrize("db_uri, expected", test_cases)
def test_get_db_details(db_uri, expected):
    with patch.dict(os.environ, {"SQLALCHEMY_DATABASE_URI": db_uri}):
        result = get_db_details()
    assert result == expected


@pytest.mark.parametrize(
    "input_db_url,expected_output",
    [
        (
            "postgresql://username:password@localhost/dbname",
            "postgresql://username:****@localhost/dbname",
        ),
        (
            "mysql+pymysql://user:secret@localhost/dbname",
            "mysql+pymysql://user:****@localhost/dbname",
        ),
        (
            "oracle+cx_oracle://user:pass@localhost:1521/sidname",
            "oracle+cx_oracle://user:****@localhost:1521/sidname",
        ),
        (
            "sqlite:///example.db",
            "sqlite:///example.db",
        ),  # No password, so no change expected
    ],
)
def test_mask_password(input_db_url, expected_output):
    assert mask_password(input_db_url) == expected_output


@pytest.mark.parametrize(
    "input_event,expected_output",
    [
        (
            {"DB_PASSWORD": "password", "other": "info"},
            {"DB_PASSWORD": "********", "other": "info"},
        ),
        (
            {"DB_PASSWORD": "short", "more": "data"},
            {"DB_PASSWORD": "*****", "more": "data"},
        ),
        (
            {"no_password": "here"},
            {"no_password": "here"},
        ),  # No DB_PASSWORD, so no change expected
    ],
)
def test_sanitize_event(input_event, expected_output):
    assert sanitize_cloudwatch_event(input_event) == expected_output
