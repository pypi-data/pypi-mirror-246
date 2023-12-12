import contextlib
from dataclasses import is_dataclass as is_dataclass
import sys
import typing
from typing import Callable, ClassVar, ForwardRef, Iterable, Mapping, Optional, Sequence, Tuple, Type, Union
from typing_extensions import (
    Annotated,
    Any,
    get_args as _typing_get_args,
    get_origin as _typing_get_origin,
    is_protocol as is_protocol,
    is_typeddict as is_typeddict,
    Literal,
)

LITERAL_TYPES: set[Any] = {Literal}
if hasattr(typing, "Literal"):
    LITERAL_TYPES.add(typing.Literal)

NoneType = type(None)
NONE_TYPES: tuple[Any, ...] = (None, NoneType, *(tp[None] for tp in LITERAL_TYPES))


def check_isinstance(value: Any, class_or_tuple: type[Any] | tuple[type[Any], ...] | None) -> bool:
    try:
        return isinstance(value, class_or_tuple)  # type: ignore[arg-type]
    except TypeError:
        return False


def check_issubclass(cls: Any, class_or_tuple: Any) -> bool:
    try:
        return isinstance(cls, type) and issubclass(cls, class_or_tuple)
    except TypeError:
        return False


def get_origin(tp: Type[Any]):
    return _typing_get_origin(tp) or getattr(tp, "__origin__", None)


def _generic_get_args(tp: Type[Any]) -> Tuple[Any, ...]:
    with contextlib.suppress(TypeError):
        if tp == Tuple[()] or sys.version_info >= (3, 9) and tp == tuple[()]:
            return ((),)
    return ()


def get_args(tp: Type[Any]) -> Tuple[Any, ...]:
    return _typing_get_args(tp) or getattr(tp, "__args__", ()) or _generic_get_args(tp)


def is_none_type(type_: Any):
    return type_ in NONE_TYPES


def is_callable_type(type_: type[Any]) -> bool:
    return type_ is Callable or get_origin(type_) is Callable


def is_literal_type(type_: type[Any]) -> bool:
    return Literal is not None and get_origin(type_) in LITERAL_TYPES


def get_literal_values(type_: type[Any]) -> tuple[Any, ...]:
    return get_args(type_)


def all_literal_values(type_: type[Any]) -> list[Any]:
    if not is_literal_type(type_):
        return [type_]

    values = get_literal_values(type_)
    return [x for value in values for x in all_literal_values(value)]


def is_annotated(type_: Any) -> bool:
    return get_origin(type_) is Annotated


def is_namedtuple(type_: type[Any]) -> bool:
    return check_issubclass(type_, tuple) and hasattr(type_, "_fields")


def _check_classvar(v: type[Any] | None) -> bool:
    if v is None:
        return False

    return v.__class__ == ClassVar.__class__ and getattr(v, "_name", None) == "ClassVar"


def is_classvar(type_: type[Any]) -> bool:
    if _check_classvar(type_) or _check_classvar(get_origin(type_)):
        return True
    if type_.__class__ == ForwardRef and type_.__forward_arg__.startswith("ClassVar["):  # type: ignore
        return True

    return False


if sys.version_info < (3, 10):

    def is_union(type_: Optional[Type[Any]]) -> bool:
        return type_ is Union


else:
    import types

    def is_union(type_: Optional[Type[Any]]) -> bool:
        return type_ is Union or type_ is types.UnionType


def is_optional(type: Type[Any]) -> bool:
    return is_union(get_origin(type)) and any(is_none_type(tp) for tp in get_args(type))


def get_type_from_optional(type: Type[Any]) -> Tuple[bool, Type[Any]]:
    if not is_optional(type):
        return False, type
    return True, next(tp for tp in get_args(type) if not is_none_type(tp))


def is_sequence_type(type: Type[Any]) -> bool:
    return check_issubclass(type, Sequence) or check_issubclass(get_origin(type), Sequence)


def is_sequence(value: Any) -> bool:
    return check_isinstance(value, Sequence)


def is_iterable_type(type: Type[Any]) -> bool:
    return check_issubclass(type, Iterable) or check_issubclass(get_origin(type), Iterable)


def is_iterable(value: Any) -> bool:
    return check_isinstance(value, Iterable)


def is_mapping_type(type: Type[Any]) -> bool:
    return check_issubclass(type, Mapping) or check_issubclass(get_origin(type), Mapping)


def is_mapping(value: Any) -> bool:
    return check_isinstance(value, Mapping)


def is_json_like_type(type_: Type[Any]) -> bool:
    return check_issubclass(type_, (Mapping, Sequence)) or check_issubclass(get_origin(type_), (Mapping, Sequence))
