from typing import Any, Callable, Set


def add_annotation(name: str, value: Any) -> Callable[[Callable], Callable]:
    """
    Decorator function to add annotations to methods or functions.

    Args:
        name: The name of the annotation.
        value: The value of the annotation.

    Returns:
        The decorated method or function.
    """

    def decorate(method: Callable) -> Callable:
        annotate(method, set, name, value)
        return method

    return decorate


def annotate(obj: Any, kind: Callable[[], Set], name: str, value: Any) -> None:
    """
    Adds an annotation to the given object.

    Args:
        obj: The object (method or function) to annotate.
        kind: The type of the annotation (a callable returning a set-like object).
        name: The name of the annotation.
        value: The value of the annotation.

    Raises:
        AssertionError: If the items associated with the annotation name is not of the expected kind.
    """
    try:
        annotations = obj.__annotations__
    except AttributeError:
        obj.__annotations__ = annotations = {}
    try:
        items = annotations[name]
    except KeyError:
        annotations[name] = items = kind()
    assert isinstance(items, kind)

    try:
        add = items.add
    except AttributeError:
        try:
            add = items.append
        except AttributeError:
            try:
                add = items.update
            except AttributeError:
                items += value
                return

    add(value)


def test_add_annotation():
    @add_annotation("author", "John")
    def my_function():
        pass

    annotations = my_function.__annotations__
    assert isinstance(annotations, dict)
    assert "author" in annotations
    assert isinstance(annotations["author"], set)
    assert "John" in annotations["author"]


def test_add_annotation_multiple_values():
    @add_annotation("tags", "python")
    @add_annotation("tags", "programming")
    def my_function():
        pass

    annotations = my_function.__annotations__
    assert isinstance(annotations, dict)
    assert "tags" in annotations
    assert isinstance(annotations["tags"], set)
    assert "python" in annotations["tags"]
    assert "programming" in annotations["tags"]


def test_add_annotation_no_value():
    @add_annotation("description", None)
    def my_function():
        pass

    annotations = my_function.__annotations__
    assert isinstance(annotations, dict)
    assert "description" in annotations
    assert isinstance(annotations["description"], set)
    assert None in annotations["description"]


def list_marked_methods(obj, marker="__marker__"):
    """
    Retrieves methods or functions from an object that have been annotated with the specified marker.

    Args:
        obj: The object to retrieve the marked methods from.
        marker: The marker attribute to check for annotations.

    Returns:
        A list of annotated methods or functions from the object.
    """
    methods = [
        getattr(obj, method_name)
        for method_name in dir(obj)
        if callable(getattr(obj, method_name))
    ]

    functions = [
        obj
        for obj in methods
        if hasattr(obj, marker) or marker in getattr(obj, "__annotations__", {})
    ]

    if callable(obj) and (
        hasattr(obj, marker) or marker in getattr(obj, "__annotations__", {})
    ):
        functions.append(obj)

    return functions


class MyClass:
    @add_annotation("marker", True)
    def method1(self):
        pass

    def method2(self):
        pass


@add_annotation("marker", True)
def my_function():
    pass


def test_list_marked_methods_class():
    obj = MyClass()
    marked_methods = list_marked_methods(obj, marker="marker")
    assert len(marked_methods) == 1
    assert obj.method1 in marked_methods
    assert obj.method2 not in marked_methods


def test_list_marked_methods_function():
    marked_functions = list_marked_methods(my_function, marker="marker")
    assert len(marked_functions) == 1
    assert my_function in marked_functions


def test_list_marked_methods_no_marker():
    obj = MyClass()
    marked_methods = list_marked_methods(obj, marker="nonexistent_marker")
    assert len(marked_methods) == 0


def test_list_marked_methods_empty_object():
    obj = object()
    marked_methods = list_marked_methods(obj, marker="marker")
    assert len(marked_methods) == 0
