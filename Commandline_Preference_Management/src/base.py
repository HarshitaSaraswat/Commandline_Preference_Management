import contextlib
from argparse import ArgumentParser
from .constants import DType, Scope


class CommandLineInterface(ArgumentParser):
    def __init__(self, args):
        super().__init__(description="Commandline Preference Management")
        self.add_argument(
            "mode", choices=["create", "read", "update", "delete"],
            help="The mode in which the command is to be run.\n`create`: To add/create a new parameter.\n`read`: To get/read a parameter.\n`update`: To update/modify a parameter value.\n`delete`: To remove/delete exinting parameter"
        )
        self.add_argument("parameter_group_path", help="The path of the parameter in the config. eg: `BaseApp/Preference/OpenGL`")
        self.add_argument("-s", "--scope", choices=[s.name for s in Scope], default=Scope.User, help="The scope of preference manipulation.")
        self.add_argument("-n", "--name", help="The name of the Preference in the given `parameter_group_path`")
        self.add_argument("-v", "--value", help="The value of the Preference for the given `name`")
        self.add_argument("-d", "--dtype", choices=[d.name for d in DType], help="The datatype of the Preference you want to access for the given `parameter_group_path`")

        self.args = self.parse_args(args)
        if self.args.dtype == "String": return
        with contextlib.suppress(Exception):
            self.args.value = int(self.args.value)
