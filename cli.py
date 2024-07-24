from flags import START_FLAG, ERROR_FLAG, EXIT_FLAG

def main():
    from Commandline_Preference_Management.src.interface import PreferenceManagementInterface
    args=[]

    with open("share", "r") as f:
        saved_interface_args = f.readline().split()
    cli = PreferenceManagementInterface(args=saved_interface_args)
    cli.run()

try:
    print(START_FLAG)
    main()
except Exception as exc:
    print(ERROR_FLAG)
    print(exc)
finally:
    print(EXIT_FLAG)