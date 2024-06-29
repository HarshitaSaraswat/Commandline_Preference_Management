from abc import ABC, abstractmethod
from .constants import Scope, DType, FCTypes
from .utils import get_parameter_group, get_freecad_method
from typing import Callable
import FreeCAD


class Command(ABC):
    @abstractmethod
    def execute(self):...


class PreferenceCommand(Command):
    _method_prefix: str

    def __init__(self, scope: Scope, parameter_group_path: str, dtype: DType):
        self.parameter_group = get_parameter_group(scope, parameter_group_path)
        self.dtype = dtype
        self.scope = scope
    
    @property
    def _method_name(self):
        return f"{self._method_prefix}{self.dtype}"

    @property
    def _executable(self) -> Callable:
        return get_freecad_method(self.parameter_group, self._method_name)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.scope}: {self.parameter_group.GetGroupName()})"


class GetPreference(PreferenceCommand):
    _method_prefix = "Get"

    def __init__(self, scope: Scope, parameter_group_path: str, name: str, dtype: DType):
        super().__init__(scope, parameter_group_path, dtype)
        self.name = name

    def execute(self):
        return self._executable(self.name)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.scope}: {self.parameter_group.GetGroupName()}.{self.name})"


class ListPreferences(PreferenceCommand):
    _method_prefix = "Get"

    @property
    def _method_name(self):
        return f"{self._method_prefix}{self.dtype}s"
    
    def execute(self):
        return self._executable()


class AddPreference(PreferenceCommand):
    _method_prefix = "Set"

    def __init__(self, scope: Scope, parameter_group_path: str, name: str, value: FCTypes, dtype: DType):
        super().__init__(scope, parameter_group_path, dtype)
        self.name = name
        self.value = value

    def execute(self):
        self._executable(self.name, self.value)
        FreeCAD.saveParameter()
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.scope}: {self.parameter_group.GetGroupName()}.{self.name}, {self.value})"


class UpdatePreference(AddPreference):...


class DeletePreference(PreferenceCommand):
    _method_prefix = "Rem"

    def __init__(self, scope: Scope, parameter_group_path: str, name: str, dtype: DType):
        super().__init__(scope, parameter_group_path, dtype)
        self.name = name

    def execute(self):
        self._executable(self.name)
        FreeCAD.saveParameter()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.scope}: {self.parameter_group.GetGroupName()}.{self.name})"