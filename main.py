from src.commands import GetPreference, AddPreference, UpdatePreference, DeletePreference, ListPreferences
from src.constants import Scope, DType


cmd = AddPreference(Scope.User, "BaseApp/Preferences/OpenGL", "my", 89, DType.Int)
cmd.execute()
cmd = UpdatePreference(Scope.User, "BaseApp/Preferences/OpenGL", "my", 333, DType.Int)
# cmd.execute()
cmd = DeletePreference(Scope.User, "BaseApp/Preferences/OpenGL", "my", DType.Int)
# cmd.execute()
cmd = GetPreference(Scope.User, "BaseApp/Preferences/OpenGL", "my", DType.Float)
print(cmd.execute())


cmd = ListPreferences(Scope.User, "BaseApp/Preferences/View", DType.String)
print(cmd.execute())