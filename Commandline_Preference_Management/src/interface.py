from argparse import ArgumentParser

from .commands import (
    AddPreference,
    DeletePreference,
    GetContent,
    GetPreference,
    ListPreferences,
    UpdatePreference,
)
from .constants import DType, Scope
from .invoker import PreferenceCommandInvoker


class CommandLineInterface(ArgumentParser):
    def __init__(self, args):
        super().__init__(description="Commandline Preference Management")
        self.add_argument("mode", choices=["create", "read", "update", "delete"])
        self.add_argument("parameter_group_path")
        self.add_argument("-s", "--scope", choices=Scope, default=Scope.User)
        self.add_argument("-n", "--name")
        self.add_argument("-v", "--value")
        self.add_argument("-d", "--dtype", choices=DType)

        # print("CommandLineInterface using args:", args)
        self.args = self.parse_args(args[1:])

    def for_add_preference(self):
        return self.args.mode == "create" and all(
            [self.args.name, self.args.value, self.args.dtype]
        )

    def for_get_preference(self):
        return (
            self.args.mode == "read"
            and all([self.args.name, self.args.dtype])
            and not self.args.value
        )

    def for_list_preferences(self):
        return (
            self.args.mode == "read"
            and self.args.dtype
            and not any([self.args.name, self.args.value])
        )

    def for_get_content(self):
        return self.args.mode == "read" and not any(
            [self.args.name, self.args.value, self.args.dtype]
        )

    def for_update_preference(self):
        return self.args.mode == "update" and all(
            [self.args.name, self.args.value, self.args.dtype]
        )

    def for_delete_preference(self):
        return (
            self.args.mode == "delete"
            and all([self.args.name, self.args.dtype])
            and not self.args.value
        )

    def detect_command(self):

        if self.for_add_preference():
            command = AddPreference(
                self.args.scope,
                self.args.parameter_group_path,
                self.args.name,
                self.args.value,
                self.args.dtype,
            )

        elif self.for_get_preference():
            command = GetPreference(
                self.args.scope,
                self.args.parameter_group_path,
                self.args.name,
                self.args.dtype,
            )

        elif self.for_update_preference():
            command = UpdatePreference(
                self.args.scope,
                self.args.parameter_group_path,
                self.args.name,
                self.args.value,
                self.args.dtype,
            )

        elif self.for_delete_preference():
            command = DeletePreference(
                self.args.scope,
                self.args.parameter_group_path,
                self.args.name,
                self.args.dtype,
            )

        elif self.for_list_preferences():
            command = ListPreferences(
                self.args.scope, self.args.parameter_group_path, self.args.dtype
            )

        elif self.for_get_content():
            command = GetContent(
                self.args.scope,
                self.args.parameter_group_path,
            )
        else:
            raise ValueError(f"Invalid combination of arguments passed: {self.args}")

        return command

    def run(self):
        command = self.detect_command()
        invoker = PreferenceCommandInvoker()
        print(invoker.execute_command(command))

