import contextlib
from argparse import ArgumentParser
from .constants import DType, Scope


class CommandLineInterface(ArgumentParser):
    def __init__(self, args):
        super().__init__(description="Commandline Preference Management")
        self.add_argument("mode", choices=["create", "read", "update", "delete"])
        self.add_argument("parameter_group_path")
        self.add_argument("-s", "--scope", choices=[s.name for s in Scope], default=Scope.User)
        self.add_argument("-n", "--name")
        self.add_argument("-v", "--value")
        self.add_argument("-d", "--dtype", choices=[d.name for d in DType])

        self.args = self.parse_args(args)
        if self.args.dtype == "String": return
        with contextlib.suppress(Exception):
            self.args.value = int(self.args.value)
