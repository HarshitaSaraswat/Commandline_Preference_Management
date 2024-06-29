from .commands import Command

class PreferenceCommandInvoker:

    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose

    def execute_command(self, cmd: Command):
        result = cmd.execute()
        if self.verbose:
            print(f"{cmd} -> {result}")
        return result