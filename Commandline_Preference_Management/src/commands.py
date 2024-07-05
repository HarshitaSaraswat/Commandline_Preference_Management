from abc import ABC, abstractmethod
from .constants import Scope, DType, FCTypes
from .utils import get_parameter_group, get_freecad_method
from typing import Callable
import FreeCAD


class Command(ABC):
    @abstractmethod
    def execute(self):
        """
        Abstract method to execute the command.

        This method should be implemented by subclasses to define the specific behavior of the command.
        """

class BasePreferenceCommand(Command):
    _method_prefix: str

    def __init__(self, scope: Scope, parameter_group_path: str):
        """
        Initializes a BasePreferenceCommand with the specified scope and parameter group path.

        Args:
            scope: The scope of the command.
            parameter_group_path: The path to the parameter group.

        Returns:
            None
        """
        self.parameter_group = get_parameter_group(scope, parameter_group_path)
        self.scope = scope
        self.parameter_group_path = parameter_group_path
    
    @property
    def _executable(self) -> Callable:
        """
        Returns the executable method for the command.

        Returns:
            The executable method for the command.
        """
        return get_freecad_method(self.parameter_group, self._method_name)
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the BasePreferenceCommand.

        Returns:
            A string representation of the BasePreferenceCommand.
        """
        return f"{self.__class__.__name__}({self.scope}: {self.parameter_group_path})"

class GetContent(BasePreferenceCommand):

    def __init__(self, scope: Scope, parameter_group_path: str):
        """
        Initializes a GetContent command with the specified scope and parameter group path.

        Args:
            scope: The scope of the command.
            parameter_group_path: The path to the parameter group.

        Returns:
            None
        """
        super().__init__(scope, parameter_group_path)

    @property
    def _executable(self) -> Callable:
        """
        Returns the executable method for the GetContent command.

        Returns:
            The executable method for the GetContent command.
        """
        return get_freecad_method(self.parameter_group, "GetContents")
    
    def execute(self):
        """
        Executes the GetContent command.

        Returns:
            The result of executing the GetContent command.
        """
        return self._executable()
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the GetContent command.

        Returns:
            A string representation of the GetContent command.
        """
        return f"{self.__class__.__name__}({self.scope}: {self.parameter_group_path})"


class PreferenceCommand(BasePreferenceCommand):
    _method_prefix: str

    def __init__(self, scope: Scope, parameter_group_path: str, dtype: DType):
        """
        Initializes a PreferenceCommand with the specified scope, parameter group path, and data type.

        Args:
            scope: The scope of the command.
            parameter_group_path: The path to the parameter group.
            dtype: The data type for the command.

        Returns:
            None
        """
        super().__init__(scope, parameter_group_path)
        self.dtype = dtype
    
    @property
    def _method_name(self):
        """
        Returns the method name for the PreferenceCommand.

        Returns:
            The method name for the PreferenceCommand.
        """
        return f"{self._method_prefix}{self.dtype}"

    @property
    def _executable(self) -> Callable:
        """
        Returns the executable method for the PreferenceCommand.

        Returns:
            The executable method for the PreferenceCommand.
        """
        return get_freecad_method(self.parameter_group, self._method_name)
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the PreferenceCommand.

        Returns:
            A string representation of the PreferenceCommand.
        """
        return f"{self.__class__.__name__}({self.scope}: {self.parameter_group_path})"


class GetPreference(PreferenceCommand):
    _method_prefix = "Get"

    def __init__(self, scope: Scope, parameter_group_path: str, name: str, dtype: DType):
        """
        Initializes a GetPreference command with the specified scope, parameter group path, name, and data type.

        Args:
            scope: The scope of the command.
            parameter_group_path: The path to the parameter group.
            name: The name of the preference.
            dtype: The data type for the command.

        Returns:
            None
        """
        super().__init__(scope, parameter_group_path, dtype)
        self.name = name

    def execute(self):
        """
        Executes the GetPreference command.

        Returns:
            The result of executing the GetPreference command.
        """
        return self._executable(self.name)
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the GetPreference command.

        Returns:
            A string representation of the GetPreference command.
        """
        return f"{self.__class__.__name__}({self.scope}: {self.parameter_group_path}.{self.name})"


class ListPreferences(PreferenceCommand):
    _method_prefix = "Get"

    @property
    def _method_name(self):
        """
        Returns the method name for listing preferences.

        Returns:
            The method name for listing preferences.
        """
        return f"{self._method_prefix}{self.dtype}s"
    
    def execute(self):
        """
        Executes the ListPreferences command.

        Returns:
            The result of executing the ListPreferences command.
        """
        return self._executable()


class AddPreference(PreferenceCommand):
    _method_prefix = "Set"

    def __init__(self, scope: Scope, parameter_group_path: str, name: str, value: FCTypes, dtype: DType):
        """
        Initializes an AddPreference command with the specified scope, parameter group path, name, value, and data type.

        Args:
            scope: The scope of the command.
            parameter_group_path: The path to the parameter group.
            name: The name of the preference.
            value: The value to set for the preference.
            dtype: The data type for the command.

        Returns:
            None
        """
        super().__init__(scope, parameter_group_path, dtype)
        self.name = name
        self.value = value

    def execute(self):
        """
        Executes the AddPreference command, sets the value for the preference, and saves the parameter.

        Returns:
            None
        """
        self._executable(self.name, self.value)
        FreeCAD.saveParameter()
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the AddPreference command.

        Returns:
            A string representation of the AddPreference command.
        """
        return f"{self.__class__.__name__}({self.scope}: {self.parameter_group_path}.{self.name}, {self.value})"


class UpdatePreference(AddPreference):...


class DeletePreference(PreferenceCommand):
    _method_prefix = "Rem"

    def __init__(self, scope: Scope, parameter_group_path: str, name: str, dtype: DType):
        """
        Initializes a DeletePreference command with the specified scope, parameter group path, name, and data type.

        Args:
            scope: The scope of the command.
            parameter_group_path: The path to the parameter group.
            name: The name of the preference.
            dtype: The data type for the command.

        Returns:
            None
        """
        super().__init__(scope, parameter_group_path, dtype)
        self.name = name

    def execute(self):
        """
        Executes the DeletePreference command, removes the specified preference, and saves the parameter.

        Returns:
            None
        """
        self._executable(self.name)
        FreeCAD.saveParameter()

    def __repr__(self) -> str:
        """
        Returns a string representation of the DeletePreference command.

        Returns:
            A string representation of the DeletePreference command.
        """
        return f"{self.__class__.__name__}({self.scope}: {self.parameter_group_path}.{self.name})"