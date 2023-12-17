import socket

import pytest


def unused_port(hostname):
    """Return a port that is unused on the current host.
    CAVEAT: race condition - a port that was free when the function checked it could be taken by another process
    by the time the function returns
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((hostname, 0))
        return s.getsockname()[1]


def test_unused_port():
    hostname = "localhost"
    port = unused_port(hostname)

    # Assert that the port is within the valid range
    assert 1024 <= port <= 65535

    # Assert that the port is currently free
    # Note: This is subject to race conditions!
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((hostname, port))
        except socket.error:
            pytest.fail("Port wasn't actually free")
