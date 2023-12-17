from pathlib import Path

import pytest

from twlib.lib.osdir.path import filter_path, scan_directory


@pytest.mark.parametrize(
    ("dir_", "expected"),
    (
        (".venv", True),
        ("/.venv", True),
        ("./noo", False),
        ("./.no.no..", False),
        ("./noo/oooo", False),
        ("./oo/nooo", False),
        ("./oo/venv/.gitter", False),
        ("./oo/venv/.git/bla/blub", True),
        ("./.venv/.git/bla/blub", True),
    ),
)
def test_filter_lks(dir_, expected):
    excludes = (".venv", ".git", "no")
    assert filter_path(Path(dir_), excludes) is expected

    # assert any(part for part in Path(dir_).parts if part in excludes)
