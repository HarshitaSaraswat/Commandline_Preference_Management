import FreeCAD
from .constants import Scope

def get_parameter_group(scope: Scope, path: str):
    return FreeCAD.ParamGet(f"{scope.value} parameter:{path}")

def get_freecad_method(parameter_group, method_name: str):
    return getattr(parameter_group, method_name)