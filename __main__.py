import subprocess
import sys
import shutil
from flags import START_FLAG, ERROR_FLAG, EXIT_FLAG

FREECAD_COMMANDS = ("freecadcmd", "FreeCADCmd")

fc_command = next(
    (command for command in FREECAD_COMMANDS if shutil.which(command)), None
)


if not fc_command:
    print(
        f"Neither of the following commands are available: {', '.join(FREECAD_COMMANDS)}"
    )
    exit(1)

command = f"{fc_command} cli.py {' '.join(sys.argv[1:])}"


output = subprocess.getoutput(command)

output = output.split(START_FLAG)[-1]
output = output.split(EXIT_FLAG)[0]
if ERROR_FLAG in output:
    output = output.split(ERROR_FLAG)[-1]
    print(output)
    exit(1)
    
print(output)
exit(0)