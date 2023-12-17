import base64
import pickle
import textwrap
from typing import Any


def serialize_to_base64(obj: Any | list, line_length=80) -> str:
    """Serialize an object to base64 string"""
    # Serialize the object to a bytes object using pickle
    serialized = pickle.dumps(obj)
    # Encode the bytes object to a base64-encoded string
    encoded = base64.b64encode(serialized).decode("utf-8")
    # Wrap the base64-encoded string every `line_length` characters
    wrapped = textwrap.fill(encoded, width=line_length)
    return wrapped


def deserialize_from_base64(base64_str: str) -> Any:
    """Deserialize a base64-encoded string to original object"""
    # Decode the base64-encoded string to a bytes object
    decoded = base64.b64decode(base64_str)
    # Deserialize the bytes object to a Python object using pickle
    obj = pickle.loads(decoded)
    return obj


FILES = [
    "file1____________________________________________________________",
    "file2____________________________________________________________",
    "file3____________________________________________________________",
    "file4____________________________________________________________",
    "file5____________________________________________________________",
    "file1____________________________________________________________",
    "file2____________________________________________________________",
    "file3____________________________________________________________",
    "file4____________________________________________________________",
    "file5____________________________________________________________",
]


def test_serialize_to_base64():
    # Serialize the list to a base64-encoded string
    serialized = serialize_to_base64(FILES)

    # Print the serialized string
    print(f"\n{serialized}")
    assert isinstance(serialized, str)


def test_deserialize_to_base64():
    serialized = """
gASVYwEAAAAAAABdlCiMQWZpbGUxX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19f
X19fX19fX19fX19fX19fX19fX19flIxBZmlsZTJfX19fX19fX19fX19fX19fX19fX19fX19fX19fX19f
X19fX19fX19fX19fX19fX19fX19fX19fX19fX1+UjEFmaWxlM19fX19fX19fX19fX19fX19fX19fX19f
X19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX5SMQWZpbGU0X19fX19fX19fX19fX19f
X19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19flIxBZmlsZTVfX19fX19f
X19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX1+UaAFoAmgD
aARoBWUu
    """
    obj = deserialize_from_base64(serialized)
    print(f"\n{obj}")
    assert obj == FILES
