import re

from dataclasses import dataclass
from typing import Annotated, Any, Dict, Optional, TypeVar, get_args, get_origin
from pydantic import Field
from pydantic.fields import FieldInfo
from pydantic._internal._fields import PydanticGeneralMetadata

from llama_prompter.types.base import TypeHandler, Type

T = TypeVar("T")


@dataclass
class CodeInfo:
    prefix: Optional[str]

    def __hash__(self) -> int:
        return hash(self.prefix)


def _regex_type(regex: str) -> Annotated[Any, ...]:
    return Annotated[str, Field(pattern=regex)]


def _code_type(prefix: Optional[str]) -> Annotated[Any, ...]:
    return Annotated[str, CodeInfo(prefix)]


def _annotated_ebnf(type_: type) -> str:
    orig_type, annotation = get_args(type_)
    if orig_type == str:
        if isinstance(annotation, CodeInfo):
            return '"```' + (annotation.prefix if annotation.prefix else "") + "\\n\" ~'.*```'s"
        else:
            for metadata in annotation.metadata:
                if hasattr(metadata, "pattern"):
                    return "~'\"" + str(metadata.pattern) + "\"'"
    assert False


def _annotated_gbnf(type_: type) -> str:
    orig_type, annotation = get_args(type_)
    if orig_type == str:
        if isinstance(annotation, CodeInfo):
            return '"```' + (annotation.prefix if annotation.prefix else "") + '\\n" [^(```)]* "```"'
        else:
            for metadata in annotation.metadata:
                if hasattr(metadata, "pattern"):
                    return '"\\"" (' + str(metadata.pattern) + ') "\\""'
    assert False


def _annotated_parser(payload: str, type_: type[T]) -> tuple[Optional[T], int]:
    orig_type, annotation = get_args(type_)
    if orig_type == str:
        if isinstance(annotation, CodeInfo):
            m = re.match("```" + (annotation.prefix or "") + "\n(.*)```", payload, re.DOTALL)
            if not m:
                return None, 0
            return m.group(1), len(m.group(0))  # type: ignore
    return Type(orig_type).parse(payload)


# Pydantic annotated types need a proper rule name in our BNF.
# Since such type may contain a lot of information, we prefer to number them (Fieldinfo1,...)
# We keep a dict of previously seen FieldInfo with an associated counter.
# Unfortunately, FieldInfo doesn't hash properly, we have to implement our how hash function.
FIELD_HASHES: Dict[int, int] = {}


def _hash_fieldinfo(field: FieldInfo) -> int:
    hashes = []
    for m in field.metadata:
        if isinstance(m, PydanticGeneralMetadata):
            hashes.append(hash(frozenset([(k, v) for k, v in m.__dict__.items()])))
        else:
            hashes.append(hash(m))
    return hash(frozenset(hashes))


def _annotated_name(type_: type) -> str:
    def _arg_name(arg_type: type) -> str:
        if isinstance(arg_type, FieldInfo):
            h = _hash_fieldinfo(arg_type)
            if h not in FIELD_HASHES:
                FIELD_HASHES[h] = len(FIELD_HASHES.keys())
            return f"Fieldinfo{FIELD_HASHES[h]}"
        elif isinstance(arg_type, CodeInfo):
            prefix = arg_type.prefix or ""
            return f"Codeinfo{prefix}"
        return Type(arg_type).name

    orig = get_origin(type_)
    assert orig
    return str(orig.__name__.lower() + "".join([_arg_name(a).title() for a in get_args(type_)]))


TypeHandler(
    lambda x: get_origin(x) == Annotated,
    _annotated_name,
    _annotated_ebnf,
    _annotated_gbnf,
    _annotated_parser,
)
