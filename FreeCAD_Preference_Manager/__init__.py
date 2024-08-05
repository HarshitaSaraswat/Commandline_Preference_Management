# PYTHON_ARGCOMPLETE_OK

from pathlib import Path
import sys
import platform
import subprocess
import shutil


FREECAD_COMMANDS = ("FreeCADCmd", "freecadcmd")

fc_command = next(
    (command for command in FREECAD_COMMANDS if shutil.which(command)), None
)

if not fc_command:
    print(
        f"Neither of the following commands are available: {', '.join(FREECAD_COMMANDS)}"
    )
    sys.exit(1)

fc_home_path = subprocess.getoutput(f"{fc_command} --get-config AppHomePath").splitlines()[-1]

os_name = platform.system()
fc_path = Path(fc_home_path)

if os_name == "Windows":
    fc_path = fc_path / "bin"
elif os_name == "Darwin":
    fc_path = fc_path / "lib"
elif os_name == "Linux":
    fc_path = fc_path / "lib"
else:
    print("Unsupported OS")
    sys.exit(1)


print(os_name)
print(fc_path)
sys.path.append(str(fc_path))

from .interface import PreferenceManagementInterface


def main():
    cli = PreferenceManagementInterface()
    cli.run()


if __name__ == "__main__":
    main()
