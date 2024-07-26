import sys
from pathlib import Path

sys.path.append(r"C:\Program Files\FreeCAD 0.21\bin")
WORKING_DIR = Path(__file__).parent.parent
sys.path.append(str(WORKING_DIR))

from src.commands import GetContent, GetPreference, AddPreference, UpdatePreference, DeletePreference, ListPreferences
from src.constants import Scope, DType
from src.invoker import PreferenceCommandInvoker

invoker = PreferenceCommandInvoker(
    verbose=True,
)


cmd = AddPreference(Scope.User, "BaseApp/Preferences/OpenGL", "my", 89, DType.Int)
invoker.execute_command(cmd)

cmd = UpdatePreference(Scope.User, "BaseApp/Preferences/OpenGL", "my", 333, DType.Int)
invoker.execute_command(cmd)

cmd = GetContent(Scope.User, "BaseApp/Preferences/OpenGL")
invoker.execute_command(cmd)

cmd = DeletePreference(Scope.User, "BaseApp/Preferences/OpenGL", "my", DType.Int)
invoker.execute_command(cmd)

cmd = GetPreference(Scope.User, "BaseApp/Preferences/OpenGL", "my", DType.Float)
invoker.execute_command(cmd)

cmd = ListPreferences(Scope.User, "BaseApp/Preferences/View", DType.String)
invoker.execute_command(cmd)


