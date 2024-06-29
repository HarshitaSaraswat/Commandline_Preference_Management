from .commands import Command
import FreeCAD
from typing import List, Any

class PreferenceCommandInvoker:
    __runtime_history: List[Command] = []

    def __init__(self, verbose: bool = False, history: bool = False, logging: bool = False) -> None:
        self.verbose = verbose
        self.history = history
        self.logging = logging

    def execute_command(self, cmd: Command) -> Any:
        result = cmd.execute()
        if self.history:
            self.__runtime_history.append(cmd)
        if self.verbose:
            print(f"{cmd} -> {result}")
        if self.logging:
            FreeCAD.Console.PrintLog(str(cmd))
        return result
    
    def print_history(self) -> List[str]:
        return [str(cmd) for cmd in self.__runtime_history]