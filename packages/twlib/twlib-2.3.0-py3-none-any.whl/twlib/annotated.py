import logging
from typing import Annotated, Any, Dict, get_type_hints

_log = logging.getLogger(__name__)


def extract_metadata(annotation: Any) -> tuple:
    """Extract metadata from an Annotated type hint."""
    origin, metadata = annotation.__origin__, annotation.__metadata__
    return origin, metadata


# Example usage:


class MyClass:
    age: Annotated[int, "Age in years"]
    height: Annotated[float, "Height in meters", "Must be positive"]
    usual: str


def get_meta_data(type_: Any) -> Dict[str, list]:
    # Extract type hints and their associated metadata
    data = {}
    for field_name, type_hint in get_type_hints(type_, include_extras=True).items():
        if getattr(type_hint, "__metadata__", None) is not None:
            field_type, metadata = extract_metadata(type_hint)
            _log.debug(
                f"Field '{field_name}' is of type '{field_type}' with metadata {metadata}"
            )
            data[field_name] = [field_type, metadata]
        else:
            _log.debug(f"Field '{field_name}' is of type '{type_hint}'")
            data[field_name] = [type_hint, ()]

    return data


def test_get_meta_data():  # type: ignore
    meta = get_meta_data(MyClass)
    assert meta.get("age") == [int, ("Age in years",)]
    assert meta.get("height") == [float, ("Height in meters", "Must be positive")]
    assert meta.get("usual") == [str, ()]
