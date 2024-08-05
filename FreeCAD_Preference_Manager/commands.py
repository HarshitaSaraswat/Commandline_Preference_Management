from abc import ABC, abstractmethod
from .constants import DType, FCTypes
from .models import (
    FCParamGroup,
    FCParamManager,
    FCParamItem,
    ParamGroupDoesNotExist,
    ParamItemDoesNotExist,
    ParamItemAlreadyExist,
)


class Command(ABC):
    @abstractmethod
    def execute(self): ...


class GetContents(Command):

    def __init__(self, param_group: FCParamGroup):
        if not param_group.exists:
            raise ParamGroupDoesNotExist(param_group)
        self.parameter_group = param_group

    def execute(self):
        return FCParamManager.get_fc_method(self.parameter_group, "GetContents")()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parameter_group.scope}: {self.parameter_group.path})"


class ListPreferences(Command):

    def __init__(self, param_group: FCParamGroup, dtype: DType):
        if not param_group.exists:
            raise ParamGroupDoesNotExist(param_group)
        self.parameter_group = param_group
        self.dtype = dtype

    def execute(self):
        return FCParamManager.get_fc_method(
            self.parameter_group, f"Get{self.dtype.name}s"
        )()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parameter_group.scope}: {self.parameter_group.path, self.dtype.name})"


class GetPreference(Command):

    def __init__(self, param_item: FCParamItem):
        if not param_item.exists:
            raise ParamItemDoesNotExist(param_item)
        self.parameter_item = param_item

    def execute(self):

        method = FCParamManager.get_fc_method(
            self.parameter_item,
            f"Get{self.parameter_item.dtype.name}",
        )
        return method(self.parameter_item.name)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parameter_item.scope}: {self.parameter_item.group_path}/{self.parameter_item.name})"


class AddPreference(Command):
    def __init__(
        self,
        param_item: FCParamItem,
        value: FCTypes,
        dtype: DType,
    ):
        if param_item.exists:
            raise ParamItemAlreadyExist(param_item)

        self.parameter_item = param_item
        self.dtype = dtype if param_item.dtype is None else param_item.dtype
        self.value = value

    def execute(self):
        method = FCParamManager.get_fc_method(
            self.parameter_item, f"Set{self.dtype.name}"
        )
        self.parameter_item.value = self.value
        self.parameter_item.dtype = self.dtype
        method(self.parameter_item.name, self.value)
        FCParamManager.save()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parameter_item.scope}: {self.parameter_item.group_path}/{self.parameter_item.name}, {self.value})"


class UpdatePreference(AddPreference):

    def __init__(
        self,
        param_item: FCParamItem,
        value: FCTypes,
    ):
        if not param_item.exists:
            raise ParamItemDoesNotExist(param_item)

        self.parameter_item = param_item
        self.dtype = param_item.dtype
        self.value = value


class DeletePreference(Command):
    def __init__(
        self,
        param_item: FCParamItem,
    ):
        if not param_item.exists:
            raise ParamItemDoesNotExist(param_item)

        self.parameter_item = param_item

    def execute(self):
        FCParamManager.get_fc_method(
            self.parameter_item, f"Rem{self.parameter_item.dtype.name}"
        )(self.parameter_item.name)
        FCParamManager.save()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.parameter_item.scope}: {self.parameter_item.group_path}.{self.parameter_item.name})"
