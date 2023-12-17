import binascii
import os
import re


def get_random_name(prefix: str = "") -> str:
    return f"{prefix}{binascii.hexlify(os.urandom(16)).decode()}"


def test_get_random_name():
    prefix = "test"
    result = get_random_name(prefix)

    # Check that the result starts with the prefix
    assert result.startswith(prefix)

    # Check that the part of the result after the prefix is a 32-character hexadecimal string
    assert re.match(r"^[0-9a-f]{32}$", result[len(prefix) :])

    # Check that without prefix still generates a 32-character hexadecimal string
    assert re.match(r"^[0-9a-f]{32}$", get_random_name())
