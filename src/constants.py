from enum import Enum
from typing import Union

class Scope(str, Enum):
    User = "User"
    Global = "Global"


class DType(str, Enum):
    Bool = "Bool"
    Float = "Float"
    Int = "Int"
    String = "String"
    Unsigned = "Unsigned"


FCTypes = Union[bool, float, int, str]