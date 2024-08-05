# PYTHON_ARGCOMPLETE_OK
from typing import List
from .constants import DType
from .models import FCParamManager


def dynamic_group_path_completer(prefix, parsed_args, **kwargs) -> List[str]:
    if parsed_args.operation != "list" and ":" in prefix:
        parent = prefix.rsplit(":", 1)[0]
        group = FCParamManager.get_group_by_path(parsed_args.scope, parent)
        return [f"{group.path}:{p.name}" for p in group.parameters]

    last_parent_path = prefix.rsplit("/", 1)[0]
    paths = FCParamManager.list_children(parsed_args.scope, last_parent_path)
    return [path for path in paths if path.startswith(prefix)]


def dtype_completer(prefix, parsed_args, **kwargs) -> List[str]:
    return [d.name for d in DType]
