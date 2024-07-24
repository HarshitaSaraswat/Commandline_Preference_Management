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