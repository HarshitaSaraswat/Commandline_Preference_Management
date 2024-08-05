# Commandline Preference Management
The FreeCAD Preference Manipulation CLI Tool will be designed to streamline the customization of FreeCAD directly from the command line interface, eliminating the need for complex graphical interfaces. It will facilitate the management of FreeCAD's preferences, enabling users to perform various tasks such as modifying existing configurations, accessing preferences stored in files, and removing unnecessary settings. Whether users are adjusting preferences for personal use or system-wide configurations, this tool will offer comprehensive control. Users will be able to swiftly create tailored preferences and make precise adjustments without the inconvenience of additional GUIs, enhancing workflow efficiency.

## Installation

### Pre-requisites
1. Python 3.11+
1. **FreeCAD** installed and `FreeCADCmd` or `freecadcmd` commands available in the system path.

### Installation
```shell
pip install git+()
```

### Autocomplete
If you want to activate autocomplete for the commandline tool, you can follow the below steps:
1. `argcomplete` package is installed with it but needs to be activated with the following command:
```shell
activate-global-python-argcomplete
```
2. Add the line below to your .bashrc (or equivalent shell)
```shell
eval "$(register-python-argcomplete freecad-preference-manager)"
source ~/.bashrc
```

### To Run
```shell
cd Commandline_Preference_Management
freecad-preference-manager arg1 arg2...
```

Use `freecad-preference-manager -h` to learn about all the available options in detail.

---

### Usages

Different combinations of options can be used to execute different commands. These combilations are listed below:
- GetContent
```shell
freecad-preference-manager list parameter_group_path
```
- ListPreferences
```shell
freecad-preference-manager list parameter_group_path -d type_of_preference
```

- GetPreference
```shell
freecad-preference-manager read parameter_group_path:preference_name
```
- AddPreference
```shell
freecad-preference-manager create parameter_group_path:preference_name -d type_of_preference -v value_of_preference
```
- UpdatePreference
```shell
freecad-preference-manager update parameter_group_path:preference_name -v value_of_preference
```
- DeletePreference
```shell
freecad-preference-manager delete parameter_group_path:preference_name
```

---


### Examples
The following example gives a simple demonstration of how to change the cursor of the python console in FreeCAD.

#### 1. read preferences for `PythonConsole`:
```shell
freecad-preference-manager list BaseApp/Preferences/PythonConsole
>>> [('Boolean', 'PythonWordWrap', True), ('Boolean', 'PythonBlockCursor', False), ('Boolean', 'SavePythonHistory', False)]
```
> This command outputs the `list` of `tuples` for each preference present.

> Tuple represents: `(datatype, property name, value)` _(in that particular order)_


#### 2. update the value of `PythonBlockCursor`:
```shell
freecad-preference-manager update BaseApp/Preferences/PythonConsole:PythonBlockCursor -v true
```

#### 3. create a new preference named `InterpreterPath`:
> **NOTE:** creating a random preference would not have any effect in FreeCAD. `InterpreterPath` is such a preference which is used here just for giving example.
```shell
freecad-preference-manager create BaseApp/Preferences/PythonConsole:InterpreterPath -d String -v path/of/python.exe
```

#### 4. read any particular value of the preference:
```shell
freecad-preference-manager read BaseApp/Preferences/PythonConsole:InterpreterPath
>>> False
```
> This command just returns the value or the provides preference name

#### 5. listing all the `Boolean` preferences in `BaseApp/Preferences/PythonConsole`
```shell
freecad-preference-manager list BaseApp/Preferences/PythonConsole -d Bool
>>> ['PythonWordWrap', 'PythonBlockCursor', 'SavePythonHistory']
```
> This command returns a `list` of the names of the parameters

#### 6. removing a parameter:
```shell
freecad-preference-manager delete BaseApp/Preferences/PythonConsole:InterpreterPath
```
