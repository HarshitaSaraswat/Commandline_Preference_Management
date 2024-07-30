# Commandline Preference Management

### Available Commands
- GetContent
- GetPreference
- AddPreference
- UpdatePreference
- DeletePreference
- ListPreferences

## Instalation
1. Clone this repository
2. Make sure that you have FreeCAD installed

### To Run
```shell
cd Commandline_Preference_Management
python . arg1 arg2...
```

```shell
usage: . {create, read, update, delete} parameter_group_path [-h] [-s {User,Global}] [-n NAME] [-v VALUE] [-d {Bool,Float,Int,String,Unsigned}] 
```

Use `python . -h` to learn about all the available options in detail.

---

### Usages

Different combinations of options can be used to execute different commands. These combilations are listed below:
- GetContent
```shell
python . read parameter_group_path
```
- GetPreference
```shell
python . read parameter_group_path -d type_of_preference -n preference_name
```
- AddPreference
```shell
python . create parameter_group_path -d type_of_preference -n preference_name -v value_of_preference
```
- UpdatePreference
```shell
python . update parameter_group_path -d type_of_preference -n preference_name -v value_of_preference
```
- DeletePreference
```shell
python . delete parameter_group_path -d type_of_preference -n preference_name
```
- ListPreferences
```shell
python . read parameter_group_path -d type_of_preference
```

---


### Examples
The following example gives a simple demonstration of how to change the cursor of the python console in FreeCAD.

#### 1. read preferences for `PythonConsole`:
```shell
python . update BaseApp/Preferences/PythonConsole
>>> [('Boolean', 'PythonWordWrap', True), ('Boolean', 'PythonBlockCursor', True), ('Boolean', 'SavePythonHistory', False)]
```
> This command outputs the `list` of `tuples` for each preference present.

> Tuple represents: `(datatype, property name, value)` _(in that particular order)_ 


#### 2. update the value of `PythonBlockCursor`:
```shell
python . update BaseApp/Preferences/PythonConsole -d Bool -n PythonBlockCursor -v true
>>> None
```
> Right now this command returns `None` on successful execution

#### 3. create a new preference named `InterpreterPath`:
> **NOTE:** creating a random preference would not have any effect in FreeCAD. `InterpreterPath` is such a preference which is used here just for giving example.
```shell
python . create BaseApp/Preferences/PythonConsole -d String -n InterpreterPath -v path/of/python.exe
>>> None
```
> Right now this command returns `None` on successful execution


#### 4. read any particular value of the preference:
```shell
python . read BaseApp/Preferences/PythonConsole -d String -n InterpreterPath
>>> False
```
> This command just returns the value or the provides preference name

#### 5. listing all the `Boolean` preferences in `BaseApp/Preferences/PythonConsole`
```shell
python . read BaseApp/Preferences/PythonConsole -d Bool
>>> ['PythonWordWrap', 'PythonBlockCursor', 'SavePythonHistory']
```
> This command returns a `list` of the names of the parameters

#### 6. removing a parameter:
```shell
python . delete BaseApp/Preferences/PythonConsole -d String -n InterpreterPath
>>> None
```
> Right now this command returns `None` on successful execution
