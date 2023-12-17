import importlib

import pytest


def _ensure_identifier(path: str, full: str) -> None:
    """
    Check that all components of the path are valid Python identifiers.

    :param path: Path to check.
    :param full: Full path (used for error message).
    :raise ValueError: If a component of the path is not a valid identifier.
    """
    for part in path.split("."):
        if part and not part.isidentifier():
            raise ValueError(
                f"Component {part!r} of {full!r} is not a valid identifier"
            )


def symbol_by_name(
    name: str,
    aliases: dict = None,
    imp: any = None,
    package: str = None,
    sep: str = ".",
    default: any = None,
    **kwargs: any,
) -> any:
    """
    Get symbol by its qualified name.

    :param name: Full dot-separated path to the class.
    :param aliases: Dict containing short name/long name mappings.
    :param imp: Module to import (default is importlib.import_module).
    :param package: Default package name.
    :param sep: Separator used in the qualified name (default is '.').
    :param default: Default value to return if import fails.
    :param kwargs: Extra arguments to pass to the imp function.
    :return: Imported module or symbol, or the default value if import fails.
    """
    imp = importlib.import_module if imp is None else imp

    if not isinstance(name, str):
        return name

    name = aliases.get(name) if aliases else name
    sep = ":" if ":" in name else sep
    module_name, _, attr = name.rpartition(sep)

    if not module_name:
        attr, module_name = None, package if package else attr

    _ensure_identifier(attr, full=name) if attr else None
    _ensure_identifier(module_name, full=name) if module_name else None

    try:
        module = imp(module_name, package=package, **kwargs)
        return getattr(module, attr) if attr else module
    except (ImportError, AttributeError):
        if default is None:
            raise
    return default


def test_symbol_by_name():
    # importing a built-in module
    result = symbol_by_name("os")
    import os

    assert result is os

    # importing a function from a built-in module
    result = symbol_by_name("os.path.join")
    assert result is os.path.join

    # importing with an alias
    aliases = {"alias": "os.path.join"}
    result = symbol_by_name("alias", aliases=aliases)
    assert result is os.path.join

    # trying to import a non-existing module
    with pytest.raises(ImportError):
        symbol_by_name("nonexistingmodule")

    # trying to import a non-existing attribute from a module
    with pytest.raises(AttributeError):
        symbol_by_name("os.nonexistingattribute")

    # importing a non-existing module with a default value
    result = symbol_by_name("nonexistingmodule", default="default")
    assert result == "default"

    # importing a non-existing attribute from a module with a default value
    result = symbol_by_name("os.nonexistingattribute", default="default")
    assert result == "default"


def test_ensure_identifier():
    # valid identifier
    _ensure_identifier("valid_identifier", "valid_identifier")

    # invalid identifier
    with pytest.raises(ValueError):
        _ensure_identifier("invalid-identifier", "invalid-identifier")
