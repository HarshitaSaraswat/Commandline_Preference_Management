import sys
from pathlib import Path

WORKING_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(WORKING_DIR))

from FreeCAD_Preference_Manager.runner.utils import START_FLAG, ERROR_FLAG, EXIT_FLAG, retrive_args
from FreeCAD_Preference_Manager.src.interface.preference import PreferenceManagementInterface

def main():
    args = retrive_args()
    cli = PreferenceManagementInterface(args=args)
    cli.run()

try:
    print(START_FLAG)
    main()
except Exception as exc:
    print(ERROR_FLAG)
    print(exc)
finally:
    print(EXIT_FLAG)
