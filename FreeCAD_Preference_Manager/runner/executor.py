import sys
import subprocess
import shutil

import os
from pathlib import Path

WORKING_DIR = Path(__file__).parent
os.chdir(WORKING_DIR)

from FreeCAD_Preference_Manager.src.interface.base import CommandLineInterface
from .utils import START_FLAG, ERROR_FLAG, EXIT_FLAG, share_args

FREECAD_COMMANDS = ("FreeCADCmd", "freecadcmd")
# INFO: different systems have different freecad commands, above two are known.

fc_command = next(
    (command for command in FREECAD_COMMANDS if shutil.which(command)), None
)
# INFO: finds the first command that is present on the system to use.

if not fc_command:
    print(
        f"Neither of the following commands are available: {', '.join(FREECAD_COMMANDS)}"
    )
    exit(1)

def run():
    cli_args = sys.argv[1:]
    CommandLineInterface(args=cli_args)

    share_args(cli_args)

    command = f"{fc_command} cli.py"
    output = subprocess.getoutput(command)

    output = output.split(START_FLAG)[-1]
    output = output.split(EXIT_FLAG)[0]
    if ERROR_FLAG in output:
        output = output.split(ERROR_FLAG)[-1]
        print(output)
        exit(1)
        
    print(output)
    exit(0)