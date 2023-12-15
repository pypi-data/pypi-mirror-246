from typing import Annotated, Any, Union
from llama_prompter.types.base import Grammar, Type

import llama_prompter.types.base_types
import llama_prompter.types.list
import llama_prompter.types.tuple
import llama_prompter.types.dict
import llama_prompter.types.pydantic  # noqa: F401
from llama_prompter.types.annotated import _regex_type, _code_type

__all__ = [
    "Grammar",
    "Type",
]

PrompterVarType = Union[type, Annotated[Any, ...]]
Regex = _regex_type
Code = _code_type
