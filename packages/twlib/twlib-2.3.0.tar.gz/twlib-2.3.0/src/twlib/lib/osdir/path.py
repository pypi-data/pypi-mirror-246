import logging
from pathlib import Path
from typing import Iterable

""" Functions which cannot be used on CLI """

_log = logging.getLogger(__name__)


def filter_path(path: Path, excludes: Iterable[str]) -> bool:
    for part in Path(path).parts:
        if part in excludes:
            _log.debug(f"Excluding {path} due to {part}")
            return True
    return False


def scan_directory(directory: Path) -> list[Path]:
    """Recursively scan directories for .md files using pathlib, skipping empty files.
    returning a list of relative paths
    """
    return [
        f.relative_to(directory)
        for f in directory.rglob("*.md")
        if f.stat().st_size > 100
    ]
