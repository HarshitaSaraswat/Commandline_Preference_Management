import sys

sys.path.append(r"C:\Program Files\FreeCAD 0.21\bin")
import FreeCAD

from FreeCAD_Preference_Manager.src.commands import GetContent, GetPreference, AddPreference, UpdatePreference, DeletePreference, ListPreferences
from FreeCAD_Preference_Manager.src.constants import Scope, DType
from FreeCAD_Preference_Manager.src.invoker import PreferenceCommandInvoker

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


