from enum import Enum
from typing import Union

class Scope(str, Enum):
    """
    An enumeration representing the scope of a preference command.

    The Scope class defines the possible scopes for preference commands, such as User or Global.
    """
    User = "User"
    Global = "Global"


class DType(str, Enum):
    """
    An enumeration representing the data type of a preference command.

    The DType class defines the possible data types for preference commands, such as Bool, Float, Int, String, and Unsigned.
    """
    Bool = "Boolean"
    Float = "Float"
    Int = "Integer"
    String = "String"
    Unsigned = "Unsigned Long"

FCTypes = Union[bool, float, int, str]

FC_TYPE_MAP = {
    "Boolean": bool,
    "Integer": int,
    "String": str,
    "Unsigned Long": int,
    "Float": float,
}
