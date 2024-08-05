from __future__ import annotations
from typing import List, Set
import FreeCAD

from .constants import DType, FCTypes, Scope


def get_parameter_group(scope: Scope, path: str) -> FreeCAD.ParameterGrp:
    if not path:
        return FreeCAD.ParamGet(f"{scope.value} parameter: BaseApp").Parent()
    return FreeCAD.ParamGet(f"{scope.value} parameter:{path}")


class FCParamItem:

    def __init__(
        self, type: str, name: str, value: FCTypes, parent: FCParamGroup
    ) -> None:
        self.dtype: DType = DType(type)
        self.name: str = name
        self.value: FCTypes = value
        self.parent: FCParamGroup = parent

        content = self.parent.fc_obj.GetContents()
        if content is None:
            self.exists = False
            return
        self.exists: bool = self.name in (c[1] for c in content)

    @property
    def group_path(self) -> str:
        return self.parent.path

    @property
    def scope(self) -> Scope:
        return self.parent.scope

    def __repr__(self) -> str:
        return f"FCParamItem({self.dtype}, {self.name}, {self.value}, {self.exists})"

    @classmethod
    def empty_item(cls, name: str, parent: FCParamGroup) -> FCParamItem:
        empty = FCParamItem("String", name, "", parent)
        empty.dtype = None  # type: ignore
        empty.value = None  # type: ignore
        empty.exists = False
        return empty


class FCParamGroup:

    def __init__(self, scope: Scope, path: str) -> None:
        if ":" in path:
            raise ValueError(
                "Group Path cannot contain ':', : is reserved for separating group and parameter name"
            )
        self.scope: Scope = scope
        self.__groups: dict[str, FCParamGroup] = {}
        self.path: str = path
        self.exists: bool = self.name in self.parent_fc_obj.GetGroups() or not path

    @property
    def name(self) -> str:
        return self.path.rsplit("/", 1)[-1]

    @property
    def groups(self) -> List[FCParamGroup]:
        return list(self.__groups.values())

    def add_group(self, group: FCParamGroup) -> None:
        self.__groups[group.name] = group

    @property
    def parameters(self) -> Set[FCParamItem]:
        if not self.exists:
            return set()
        content = self.fc_obj.GetContents()
        if content is None:
            return set()
        return {FCParamItem(*param, parent=self) for param in content}

    @property
    def fc_obj(self) -> FreeCAD.ParameterGrp:
        return get_parameter_group(self.scope, self.path)

    @property
    def parent_fc_obj(self) -> FreeCAD.ParameterGrp:
        path_split = self.path.rsplit("/", 1)
        if len(path_split) == 1:
            return get_parameter_group(self.scope, "")
        return get_parameter_group(self.scope, path_split[0])

    def populate(self) -> None:
        for gn in self.fc_obj.GetGroups():
            group = FCParamGroup(self.scope, f"{self.path}/{gn}")
            self.add_group(group)

    def __getitem__(self, item) -> FCParamItem:
        try:
            return next(filter(lambda x: x.name == item, self.parameters))
        except StopIteration as e:
            raise KeyError(f"Parameter {item} not found in {self.path}") from e

    def __repr__(self) -> str:
        return f"FCParamGroup({self.scope}, {self.path}, {self.exists})"


class FCParamManager:

    @staticmethod
    def get_group_by_path(scope: Scope, path: str) -> FCParamGroup:
        nodes_names = path.split("/")
        param_node = FCParamGroup(scope, "")
        for i, nn in enumerate(nodes_names):
            next_node = FCParamGroup(scope, f"{param_node.path}/{nn}" if i > 0 else nn)
            param_node.add_group(next_node)
            param_node = next_node

        return param_node

    @staticmethod
    def get_parameter_by_path(scope: Scope, path: str) -> FCParamItem:
        if ":" not in path:
            raise ValueError("Group Path and parameter name should be separated by ':'")

        group_path, param_name = path.rsplit(":", 1)
        group = FCParamManager.get_group_by_path(scope, group_path)
        try:
            return group[param_name]
        except KeyError as e:
            return FCParamItem.empty_item(param_name, group)

    @staticmethod
    def construct_param_group_tree(scope: Scope, path: str) -> FCParamGroup:
        root = FCParamManager.get_group_by_path(scope, path)
        root.populate()

        def populate_tree(node: FCParamGroup) -> None:
            node.populate()
            for group in node.groups:
                populate_tree(group)

        populate_tree(root)
        return root

    @staticmethod
    def list_all_group_paths(scope: Scope, root: str = "") -> List[str]:

        paths = []
        def list_paths(node: FCParamGroup) -> None:
            if node.path:
                paths.append(node.path)
            for group in node.groups:
                list_paths(group)

        list_paths(FCParamManager.construct_param_group_tree(scope, root))

        return paths

    @staticmethod
    def list_children(scope: Scope, path: str) -> List[str]:
        group = FCParamManager.get_group_by_path(scope, path)
        group.populate()
        return [f"{group.path}/{g.name}" for g in group.groups]

    @staticmethod
    def get_fc_method(fc_param: FCParamGroup | FCParamItem, method_name: str):
        if isinstance(fc_param, FCParamItem):
            fc_param = fc_param.parent
        return getattr(fc_param.fc_obj, method_name)

    @staticmethod
    def save() -> None:
        FreeCAD.saveParameter()


class ParamGroupDoesNotExist(ValueError):
    def __init__(self, obj: FCParamGroup) -> None:
        super().__init__(f"Parameter group with path {obj.path} does not exist")


class ParamItemDoesNotExist(ValueError):
    def __init__(self, obj: FCParamItem) -> None:
        super().__init__(f"Parameter {obj.name} not found in group {obj.group_path}")


class ParamItemAlreadyExist(ValueError):
    def __init__(self, obj: FCParamItem) -> None:
        super().__init__(f"Parameter {obj.name} exists in group {obj.group_path}")
