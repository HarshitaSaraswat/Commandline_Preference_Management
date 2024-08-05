from .commands import Command
import FreeCAD
from typing import List, Any

class PreferenceCommandInvoker:
    """
    A class to execute and manage command preferences.

    Args:
        verbose: A boolean indicating whether to display verbose output.
        history: A boolean indicating whether to keep a history of executed commands.
        logging: A boolean indicating whether to log command executions.

    Methods:
        execute_command(cmd): Executes a given command and returns the result.
        print_history(): Returns a list of strings representing the command history.
    """

    __runtime_history: List[Command] = []

    def __init__(self, verbose: bool = False, history: bool = False, logging: bool = False) -> None:
        """
        Initializes the PreferenceCommandInvoker with specified options.

        Args:
            verbose: A boolean indicating whether to display verbose output.
            history: A boolean indicating whether to keep a history of executed commands.
            logging: A boolean indicating whether to log command executions.
        """

        self.verbose = verbose
        self.history = history
        self.logging = logging

    def execute_command(self, cmd: Command) -> Any:
        """
        Executes a given command and returns the result.

        Args:
            cmd: The command to be executed.

        Returns:
            The result of the command execution.
        """

        result = cmd.execute()
        if self.history:
            self.__runtime_history.append(cmd)
        if self.verbose:
            print(f"{cmd} -> {result}")
        if self.logging:
            FreeCAD.Console.PrintLog(str(cmd))
        return result
    
    def print_history(self) -> List[str]:
        """
        Returns a list of strings representing the command history.

        Returns:
            A list of strings representing the command history.
        """

        return [str(cmd) for cmd in self.__runtime_history]
