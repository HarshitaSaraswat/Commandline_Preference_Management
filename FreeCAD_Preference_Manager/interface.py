# PYTHON_ARGCOMPLETE_O

import argparse
import argcomplete
from .constants import DType, Scope
from .commands import (
    AddPreference,
    DeletePreference,
    GetContents,
    GetPreference,
    ListPreferences,
    UpdatePreference,
)
from .invoker import PreferenceCommandInvoker
from .models import FCParamManager
from .autocompleter import dynamic_group_path_completer, dtype_completer


class PreferenceManagementInterface:

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Commandline Preference Management"
        )

        self.parser.add_argument(
            "-s",
            "--scope",
            choices=[s.name for s in Scope],
            default=Scope.User,
            help="The scope of preference manipulation.",
        )

        self.subparsers = self.parser.add_subparsers(dest="operation", required=True)

        self.create_parser = self.subparsers.add_parser(
            "create", help="Create operation"
        )
        self.create_parser.add_argument(
            "path",
            type=str,
            help="The path to the new parameter to be created including the name",
        ).completer = dynamic_group_path_completer
        self.create_parser.add_argument(
            "-d",
            "--dtype",
            type=str,
            choices=[d.name for d in DType],
            help="Data type of the parameter to be created",
            required=True,
        ).completer = dtype_completer
        self.create_parser.add_argument(
            "-v",
            "--value",
            type=str,
            required=True,
            help="Value of the parameter to be created",
        )

        self.read_parser = self.subparsers.add_parser("read", help="Read operation")
        self.read_parser.add_argument(
            "path",
            help="The path of the parameter to be read",
        ).completer = dynamic_group_path_completer

        self.list_parser = self.subparsers.add_parser("list", help="Read operation")
        self.list_parser.add_argument(
            "path",
            help="The path of the parameter group to be listed",
        ).completer = dynamic_group_path_completer
        self.list_parser.add_argument(
            "-d",
            "--dtype",
            type=str,
            choices=[d.name for d in DType],
            help="Data type of the parameter to be updated(can be different from the existing one)",
        ).completer = dtype_completer

        self.update_parser = self.subparsers.add_parser(
            "update", help="Update operation"
        )
        self.update_parser.add_argument(
            "path",
            help="The path of the parameter to be updated",
        ).completer = dynamic_group_path_completer
        self.update_parser.add_argument(
            "-v",
            "--value",
            type=str,
            help="Value of the parameter to be updated",
            required=True,
        )

        self.delete_parser = self.subparsers.add_parser(
            "delete", help="Delete operation"
        )
        self.delete_parser.add_argument(
            "path",
            help="The path of the parameter to be deleted",
        ).completer = dynamic_group_path_completer

        argcomplete.autocomplete(self.parser)
        self.args = self.parser.parse_args()

        if hasattr(self.args, "dtype") and self.args.dtype is not None:
            self.args.dtype = DType[self.args.dtype]

        if self.args.operation == "list":
            self.group = FCParamManager.get_group_by_path(
                self.args.scope, self.args.path
            )
            return
        else:
            self.item = FCParamManager.get_parameter_by_path(
                self.args.scope, self.args.path
            )

        if self.args.operation in ("create", "update"):
            item_dtype = (
                self.args.dtype if hasattr(self.args, "dtype") else self.item.dtype
            )

            if item_dtype == DType.Bool:
                self.args.value = self.args.value in ["1", "True", "true"]

            elif item_dtype == DType.Float:
                self.args.value = float(self.args.value)

            elif item_dtype in [DType.Int, DType.Unsigned]:
                self.args.value = int(self.args.value)

    def detect_command(self):

        if self.args.operation == "create":
            command = AddPreference(
                self.item,
                self.args.value,
                self.args.dtype,
            )

        elif self.args.operation == "read":
            command = GetPreference(self.item)

        elif self.args.operation == "update":
            command = UpdatePreference(
                self.item,
                self.args.value,
            )

        elif self.args.operation == "delete":
            command = DeletePreference(self.item)

        elif self.args.operation == "list" and not self.args.dtype:
            command = GetContents(self.group)

        elif self.args.operation == "list":
            command = ListPreferences(
                self.group,
                self.args.dtype,
            )

        else:
            raise ValueError(f"Invalid combination of arguments passed: {self.args}")

        return command

    def run(self):
        output = self._run()
        if output is None:
            return
        print(output)

    def _run(self):
        command = self.detect_command()
        invoker = PreferenceCommandInvoker()
        return invoker.execute_command(command)
