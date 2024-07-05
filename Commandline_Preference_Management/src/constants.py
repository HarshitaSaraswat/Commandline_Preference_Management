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
    Bool = "Bool"
    Float = "Float"
    Int = "Int"
    String = "String"
    Unsigned = "Unsigned"


FCTypes = Union[bool, float, int, str]