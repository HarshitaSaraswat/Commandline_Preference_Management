import subprocess
import sys
from flags import START_FLAG, ERROR_FLAG, EXIT_FLAG

command = f"FreeCADCmd cli.py {' '.join(sys.argv[1:])}"

output = subprocess.getoutput(command)

output = output.split(START_FLAG)[-1]
output = output.split(EXIT_FLAG)[0]
if ERROR_FLAG in output:
    output = output.split(ERROR_FLAG)[-1]
    
print(output)